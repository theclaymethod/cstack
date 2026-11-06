#!/usr/bin/env python3
"""Write a separate local eval handoff from a selected structured findings packet."""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import shutil
import tempfile


IDENTIFIERS = {"example_id", "record_id", "amends", "rubric_id", "source_id", "origin_source_id",
               "item_id", "artifact_id", "input_ref", "output_ref", "criterion_id", "id",
               "schema_version", "version", "label", "status", "passing_answer", "answer"}


class PrivacyFilter:
    def __init__(self, checkpoint, device):
        from opf import OPF
        if not (checkpoint / "config.json").is_file() or not any(checkpoint.glob("*.safetensors")):
            raise ValueError("Expected an existing local OPF checkpoint")
        self.model = OPF(model=str(checkpoint.resolve()), device=device)

    def __call__(self, text, context=""):
        prefix = f"Field: {context}\nValue: "
        result = self.model.redact(prefix + text)
        if result.warning or result.summary.get("decoded_mismatch"):
            raise ValueError("Redaction offsets need private review")
        # OPF's structured result also holds original text and detected span text.
        cursor, pieces = 0, []
        for span in result.detected_spans:
            start, end = max(0, span.start - len(prefix)), min(len(text), span.end - len(prefix))
            if end <= start:
                continue
            if start < cursor:
                raise ValueError("Overlapping redaction spans need private review")
            pieces.extend((text[cursor:start], span.placeholder))
            cursor = end
        return "".join(pieces) + text[cursor:]


def sanitize(value, redact, counts, context=""):
    if isinstance(value, str) or type(value) in (int, float):
        text = value if isinstance(value, str) else str(value)
        cleaned = redact(text, context)
        if not isinstance(cleaned, str):
            raise ValueError("Redactor must return text")
        counts["values_processed"] += 1
        counts["values_changed"] += cleaned != text
        return value if cleaned == text else cleaned
    if isinstance(value, list):
        return [sanitize(item, redact, counts, context) for item in value]
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if redact(key, "JSON field name") != key:
                raise ValueError("Use neutral field names before export")
            cleaned = sanitize(item, redact, counts, key)
            if (key in IDENTIFIERS or key.endswith(("_id", "_ids"))) and cleaned != item:
                raise ValueError("Replace identifying references with consistent opaque IDs before export")
            result[key] = cleaned
        if "replay_ready" in result:
            result.setdefault("capture_replay_ready", result["replay_ready"])
            result["replay_ready"] = False
        return result
    if value is None or type(value) in (bool, int, float):
        return value
    raise ValueError("Expected JSON data")


HANDOFF = """# Eval author handoff

Use findings.json as evidence for constructing evals. One example is one specific
expert judgment. Preserve uncertainty, preferences, retractions, criterion versions,
and expert-endorsed alternatives. History is provenance, not extra independent rows.

Review privacy and intent separately. Confirm that masking preserved the failure,
correction, units, relationships, conditions, and applicability. Keep a changed or
incomplete example provisional. Capture readiness is not post-export readiness.

Materialized input/output context and an observable criterion are required for a
repeatable task. A scoped binary criterion can suffice without a full replacement.
Do not infer gold answers, numerical tolerances, endorsements, or population claims.

After local review, save review.json referencing findings.json's current SHA-256,
with privacy_review and intent_review verdicts, unresolved limits, and reviewer
provenance suitable for the intended audience. Recheck if the file changes. The
manifest records processing, not a guarantee of anonymization or permission to share.
Keep raw sources and any identity lookup outside the bundle. Sharing is a separate
user-directed action; this tool only writes local files.
"""


def export_packet(packet, destination, redact, privacy):
    if packet.get("schema_version") != 1:
        raise ValueError("Expected packet schema_version 1")
    for field in ("examples", "rubric"):
        if not isinstance(packet.get(field), list) or not all(isinstance(x, dict) for x in packet[field]):
            raise ValueError("Expected example and rubric arrays")
    if destination.exists():
        raise FileExistsError("Export destination must be new")
    counts = {"values_processed": 0, "values_changed": 0}
    cleaned = sanitize(packet, redact, counts)
    cleaned["export_review_required"] = True
    cleaned["source_representation"] = "Export projection; private originals are the authority for exact source text."
    content = (json.dumps(cleaned, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()
    manifest = {"schema_version": 1, "created_at": datetime.now(timezone.utc).isoformat(),
                "files": {"findings.json": hashlib.sha256(content).hexdigest(),
                          "HANDOFF.md": hashlib.sha256(HANDOFF.encode()).hexdigest()},
                "examples": len(cleaned["examples"]), "rubric_definitions": len(cleaned["rubric"]),
                "privacy_processing": privacy, "redaction": counts,
                "privacy_review": "required", "intent_review": "required", "shareability": "not_assessed"}
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".eval-export-", dir=destination.parent))
    try:
        for name, data in (("findings.json", content), ("HANDOFF.md", HANDOFF.encode()),
                           ("manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())):
            path = staging / name
            path.write_bytes(data)
            path.chmod(0o600)
        if destination.exists():
            raise FileExistsError("Export destination must be new")
        staging.rename(destination)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("destination", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--checkpoint", type=Path, help="Existing local OPF checkpoint; never auto-downloads")
    mode.add_argument("--already-redacted", action="store_true", help="Explicit manual/external preparation; no model scan")
    parser.add_argument("--revision-file", type=Path, help="Local file containing the downloaded model's 40-character revision")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    args = parser.parse_args()
    try:
        # The checkpoint and tokenization assets must already be local.
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        if args.checkpoint:
            redact = PrivacyFilter(args.checkpoint, args.device)
            revision = args.revision_file.read_text().strip() if args.revision_file else None
            if revision is not None and not re.fullmatch(r"[0-9a-f]{40}", revision):
                raise ValueError("Expected a model commit revision")
            privacy = {"method": "openai/privacy-filter", "opf_version": version("opf"),
                       "model_revision": revision, "revision_source": "operator_provided" if revision else "unrecorded",
                       "device": args.device, "inference": "local", "scan_unit": "JSON keys and string/numeric values with field-name context"}
        else:
            if args.revision_file:
                raise ValueError("Revision file requires a checkpoint")
            redact = lambda text, context: text
            privacy = {"method": "operator_prepared", "model_scan": False}
        if args.packet.stat().st_size > 10_000_000:
            raise ValueError("Select a packet smaller than 10 MB")
        with args.packet.open("rb") as handle:
            raw = handle.read(10_000_001)
        if len(raw) > 10_000_000:
            raise ValueError("Select a packet smaller than 10 MB")
        export_packet(json.loads(raw), args.destination, redact, privacy)
    except Exception:
        parser.exit(1, "Export stopped. No completed bundle was written. Inspect input/setup privately; source text is omitted from this error.\n")
    print("Local bundle written; privacy and eval-intent review remain required.")


if __name__ == "__main__":
    main()

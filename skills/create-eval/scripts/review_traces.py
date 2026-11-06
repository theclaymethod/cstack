#!/usr/bin/env python3
"""Review a selected local JSONL trace snapshot; append reviewer evidence to JSONL."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
from uuid import uuid4


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_jsonl(path, snapshot=None):
    records = []
    source = snapshot.decode("utf-8") if snapshot is not None else path.read_text(encoding="utf-8")
    for number, line in enumerate(source.splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except ValueError as exc:
            raise ValueError(f"{path.name}:{number}: invalid JSON") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{path.name}:{number}: expected an object")
        records.append(record)
    return records


def load_traces(path, snapshot=None):
    records = read_jsonl(path, snapshot)
    seen = set()
    rows = []
    for trace in records:
        trace_id = trace.get("id")
        if not isinstance(trace_id, str) or not trace_id.strip() or trace_id in seen:
            raise ValueError("Trace IDs must be nonempty, unique strings")
        if "input" not in trace:
            raise ValueError(f"Trace {trace_id}: missing input")
        if "output" not in trace and "error" not in trace:
            raise ValueError(f"Trace {trace_id}: missing output or error")
        seen.add(trace_id)
        rows.append({"trace": trace, "sha256": hashlib.sha256(canonical(trace).encode()).hexdigest()})
    if not rows:
        raise ValueError("No traces to review")
    return rows


class ReviewServer(HTTPServer):
    def __init__(self, address, traces_path, reviews_path, reviewer):
        snapshot = traces_path.read_bytes()
        self.rows = load_traces(traces_path, snapshot)
        self.by_id = {row["trace"]["id"]: row for row in self.rows}
        self.snapshot_hash = hashlib.sha256(snapshot).hexdigest()
        self.reviews_path = reviews_path
        self.history = read_jsonl(reviews_path) if reviews_path.exists() else []
        self.latest = {}
        for event in self.history:
            required = {"record_id", "review_id", "trace_id", "trace_sha256", "verdict", "scope", "reviewer"}
            if not required.issubset(event):
                raise ValueError("Review file is not this tool's annotation history")
            if any(not isinstance(event[key], str) for key in required):
                raise ValueError("Invalid review history fields")
            self.latest[event["review_id"]] = event
        self.reviewer = reviewer
        self.token = secrets.token_urlsafe(32)
        self.assets = Path(__file__).resolve().parent.parent / "assets"
        super().__init__(address, ReviewHandler)

    def save_review(self, body):
        row = self.by_id.get(body.get("trace_id"))
        if row is None or body.get("trace_sha256") != row["sha256"]:
            raise ValueError("Trace changed or is outside this review snapshot")
        review_id = body.get("review_id")
        if not isinstance(review_id, str) or not review_id.strip() or len(review_id) > 100:
            raise ValueError("Invalid review ID")
        previous = self.latest.get(review_id)
        if previous and (previous["trace_id"] != body["trace_id"] or previous["trace_sha256"] != row["sha256"]):
            raise ValueError("An existing review cannot be reassigned to another trace version")
        if body.get("amends") != (previous["record_id"] if previous else None):
            raise RuntimeError("Review changed in another tab; reload before saving")
        verdict = body.get("verdict")
        if verdict not in {"UNREVIEWED", "PASS", "FAIL", "DEFER"}:
            raise ValueError("Invalid verdict")
        fields = {}
        for name in ("reviewer", "scope", "notes", "correction"):
            value = body.get(name, "")
            if not isinstance(value, str):
                raise ValueError(f"{name} must be text")
            fields[name] = value.strip()
        if not fields["reviewer"] or not fields["scope"]:
            raise ValueError("Reviewer and judgment scope are required")
        if verdict == "UNREVIEWED" and not fields["notes"] and not fields["correction"]:
            raise ValueError("Add an observation or select a verdict")
        questions = body.get("rubric_questions", [])
        if not isinstance(questions, list) or any(not isinstance(q, str) or not q.strip() for q in questions):
            raise ValueError("Rubric questions must be nonempty text")
        event = {
            "schema_version": 1,
            "record_id": str(uuid4()),
            "review_id": review_id,
            "amends": previous["record_id"] if previous else None,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "trace_id": body["trace_id"],
            "trace_sha256": row["sha256"],
            "snapshot_sha256": self.snapshot_hash,
            "verdict": verdict,
            **fields,
            "correction": fields["correction"] or None,
            "rubric_questions": questions,
            "rubric_status": "proposed" if questions else None,
        }
        self.reviews_path.parent.mkdir(parents=True, exist_ok=True)
        # One server serializes its writes. Reject observed external changes;
        # callers must use only one server per review file.
        current = read_jsonl(self.reviews_path) if self.reviews_path.exists() else []
        if current != self.history:
            raise RuntimeError("Review file changed outside this server; restart to load it")
        # Validate a trailing newline so an interrupted record cannot be joined.
        if self.reviews_path.exists() and self.reviews_path.stat().st_size:
            with self.reviews_path.open("rb") as source:
                source.seek(-1, os.SEEK_END)
                if source.read(1) != b"\n":
                    raise RuntimeError("Review file lacks its final newline; inspect before appending")
        descriptor = os.open(self.reviews_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        with os.fdopen(descriptor, "a", encoding="utf-8") as destination:
            destination.write(canonical(event) + "\n")
            destination.flush()
            os.fsync(destination.fileno())
        self.history.append(event)
        self.latest[review_id] = event
        return event


class ReviewHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def send(self, status, content, mime="application/json; charset=utf-8"):
        data = content if isinstance(content, bytes) else canonical(content).encode()
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def authorized(self):
        expected = "Bearer " + self.server.token
        return secrets.compare_digest(self.headers.get("Authorization", ""), expected)

    def do_GET(self):
        assets = {"/": ("trace-review.html", "text/html; charset=utf-8"),
                  "/app.js": ("trace-review.js", "text/javascript; charset=utf-8"),
                  "/style.css": ("trace-review.css", "text/css; charset=utf-8")}
        if self.path in assets:
            filename, mime = assets[self.path]
            self.send(200, (self.server.assets / filename).read_bytes(), mime)
        elif self.path == "/api/data":
            if not self.authorized():
                self.send(403, {"error": "Open the launch URL from the terminal"})
                return
            self.send(200, {"rows": self.server.rows, "reviews": list(self.server.latest.values()), "reviewer": self.server.reviewer})
        else:
            self.send(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/api/reviews":
            self.send(404, {"error": "Not found"})
            return
        if not self.authorized():
            self.send(403, {"error": "Open the launch URL from the terminal"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 1_000_000:
                raise ValueError("Invalid annotation size")
            body = json.loads(self.rfile.read(size))
            if not isinstance(body, dict):
                raise ValueError("Expected an annotation object")
            self.send(200, self.server.save_review(body))
        except RuntimeError as exc:
            self.send(409, {"error": str(exc)})
        except (ValueError, TypeError, KeyError) as exc:
            self.send(400, {"error": str(exc)})
        except OSError:
            self.send(500, {"error": "Could not persist review; inspect the local output path"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traces", type=Path, help="Selected development traces, one JSON object per line")
    parser.add_argument("--reviews", type=Path, required=True, help="Append-only local review JSONL")
    parser.add_argument("--reviewer", default="", help="Prefill the reviewer name; can be edited in the UI")
    parser.add_argument("--port", type=int, default=0, help="Local port; default chooses an available port")
    args = parser.parse_args()
    if args.traces.resolve() == args.reviews.resolve():
        parser.error("Trace input and review output must be separate files")
    try:
        server = ReviewServer(("127.0.0.1", args.port), args.traces, args.reviews, args.reviewer)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"http://127.0.0.1:{server.server_port}/#{server.token}", flush=True)
    print(f"Reviewing {len(server.rows)} traces. Saving to {args.reviews}. Stop with Ctrl+C.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

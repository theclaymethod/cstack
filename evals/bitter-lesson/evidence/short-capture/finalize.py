"""Index existing exercise evidence without executing a candidate."""
import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
workspace = root.parents[1]
skills = root / "source/installed-skills"
skills.mkdir(parents=True, exist_ok=True)
for rel in ["expert-mode/SKILL.md", "expert-mode/references/records.md", "distill-me/SKILL.md"]:
    target = skills / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(workspace / ".agents/skills" / rel, target)
for name in ("cstack-skills.lock.json", ".cstack-source.json"):
    shutil.copy2(workspace / name, root / "source" / name)
versions = json.loads((root / "native-versions.json").read_text())
trace = json.loads((root / "native/regenerated/traces.jsonl").read_text())
versions["regenerated"] = {
    "native_receipt": "native/regenerated/manifest.json", "trace": "native/regenerated/traces.jsonl",
    "case": trace["id"], "input": trace["input"], "output": trace["output"],
    "source": "native/regenerated/candidate.py", "grade": "PASS",
    "scripted_reviewer_judgment": None, "expert_reassessment": None,
    "inherited_judgment": None, "status": "new local demonstration output, not canonical replacement"}
(root / "native-versions.json").write_text(json.dumps(versions, indent=2, sort_keys=True) + "\n")
manifest = {
    "schema_version": 1, "task": "controlled capture and retrospective merge", "capture_active": False,
    "native_case_budget": 48, "native_case_executions": 2, "remaining_case_budget": 46,
    "native_runs": {"baseline": "native/baseline", "regenerated": "native/regenerated"},
    "raw_source": "source/review-session.md", "reviews": "reviews.jsonl", "rubric": "rubric.jsonl",
    "excluded_proposals": "excluded-proposals.jsonl", "output_versions": "native-versions.json",
    "checkpoints": ["checkpoints/first", "checkpoints/stopped", "checkpoints/merge1", "checkpoints/merge2"],
    "driver": "driver.py", "commands": "commands.txt", "report": "REPORT.md",
    "verification": "verification.json", "source_authority": "synthetic scripted source only",
    "hashes": {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted(root.rglob("*")) if p.is_file() and p != root / "manifest.json"}}
(root / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
print(json.dumps({"manifest": "manifest.json", "files_hashed": len(manifest["hashes"]),
                  "actual_native_case_executions": 2}))

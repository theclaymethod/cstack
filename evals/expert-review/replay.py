#!/usr/bin/env python3
"""Replay preserved data submissions through trusted prepare/capture/grade commands."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--grader", type=Path, default=Path(__file__).parent / "run.py")
    parser.add_argument("--submissions", type=Path,
                        default=Path(__file__).parent / "evidence/round-1/submissions.json")
    args = parser.parse_args()
    args.destination.mkdir(parents=True, exist_ok=False)
    submissions = json.loads(args.submissions.read_text())
    summary = []
    for submission in submissions:
        name = submission.get("name", submission["case"])
        if not isinstance(name, str) or not name or Path(name).name != name or name in (".", ".."):
            raise ValueError("Expected a simple submission name")
        location = args.destination / name
        work, operator = location / "work", location / "operator"
        command = [sys.executable, str(args.grader.resolve())]
        subprocess.run(command + ["prepare", submission["case"], str(work), str(operator)], check=True)
        for step in submission["steps"]:
            for filename in ("reviews.jsonl", "rubric.jsonl", "reply.md"):
                path = work / filename if filename == "reply.md" else work / "dataset" / filename
                path.write_text(step[filename])
            subprocess.run(command + ["capture", str(operator)], check=True, capture_output=True)
        result = subprocess.run(command + ["grade", str(operator)], text=True, capture_output=True)
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)
        graded = json.loads(result.stdout)
        (location / "result.json").write_text(result.stdout)
        summary.append({"name": name, "artifact_checks_passed": graded["artifact_checks_passed"],
                        "grader_version": graded["grader_version"], "exit_code": result.returncode})
    (args.destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

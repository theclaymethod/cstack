#!/usr/bin/env python3
"""Checks that tutor progress appends, resumes, and refuses to erase work."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "progress.py"


def workspace(root):
    for relative in ("evaluate.py", "support_agent.py", "exercises/01-expert-mode.md", "evals/spec.json", "evals/cases.jsonl"):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n")
    (root / ".cstack-source.json").write_text('{"source": "/cstack"}\n')


def run(root, *args):
    return subprocess.run([sys.executable, str(SCRIPT), "--workspace", str(root), *args], text=True, capture_output=True)


def record(root, name, **fields):
    payload = {"stage": "orient", "learner_response": "", "observation": "shown the trace", "unresolved": [], "next_action": "Ask one question.", "completed": [], "artifacts": []}
    payload.update(fields)
    path = root / name
    path.write_text(json.dumps(payload))
    return path


class ProgressTests(unittest.TestCase):
    def test_checkpoint_is_append_only_and_status_rebuilds_from_the_journal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace(root)
            doctor = run(root, "doctor")
            self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
            draft = record(root, "draft.json", learner_response="For this output, guidance without a ticket.", assistance="independent",
                           artifacts=["evals/spec.json"])
            saved = run(root, "checkpoint", "--record", str(draft), "--expected", "0")
            self.assertEqual(saved.returncode, 0, saved.stderr)
            self.assertEqual(json.loads(saved.stdout)["revision"], 1)
            conflict = run(root, "checkpoint", "--record", str(draft), "--expected", "0")
            self.assertNotEqual(conflict.returncode, 0)
            self.assertIn("Do not overwrite", conflict.stderr)
            self.assertTrue((root / "eval-runs/tutor/progress/events/000001.json").is_file())
            (root / "evals/spec.json").write_text("changed\n")
            (root / "eval-runs/tutor/progress/state.json").unlink()
            status = json.loads(run(root, "status").stdout)
            self.assertEqual(status["revision"], 1)
            self.assertEqual(status["last_learner_response"], "For this output, guidance without a ticket.")
            self.assertEqual(status["changed_or_missing"], [{"path": "evals/spec.json", "status": "changed"}])

    def test_completed_work_stays_in_order_and_prior_decisions_remain(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace(root)
            first = record(root, "one.json", stage="01-expert-mode", completed=["01-expert-mode"],
                           learner_response="Creating a ticket was wrong.", decisions={"how_to": "guidance"},
                           next_action="Ask what stayed uncertain.")
            self.assertEqual(run(root, "checkpoint", "--record", str(first), "--expected", "0").returncode, 0)
            skip = record(root, "skip.json", stage="02-distill-me", completed=["01-expert-mode", "03-bootstrap"],
                          next_action="Nope.")
            skipped = run(root, "checkpoint", "--record", str(skip), "--expected", "1")
            self.assertNotEqual(skipped.returncode, 0)
            erase = record(root, "erase.json", stage="orient", completed=[], next_action="Start over.")
            self.assertNotEqual(run(root, "checkpoint", "--record", str(erase), "--expected", "1").returncode, 0)
            second = record(root, "two.json", stage="02-distill-me", completed=["01-expert-mode"],
                            learner_response="The urgency line was not a decision.", decisions={"urgency": "unresolved"},
                            next_action="Show the duplicate merge.")
            merged = run(root, "checkpoint", "--record", str(second), "--expected", "1")
            self.assertEqual(merged.returncode, 0, merged.stderr)
            status = json.loads(run(root, "status").stdout)
            self.assertEqual(status["completed"], ["01-expert-mode"])
            self.assertEqual(status["decisions"]["how_to"], "guidance")
            self.assertEqual(status["decisions"]["urgency"], "unresolved")
            self.assertFalse((root / "eval-runs/tutor/progress/events/000003.json").exists())

    def test_canonical_fixture_is_not_a_progress_store(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "exercises").mkdir()
            (root / "exercises/01-expert-mode.md").write_text("# 01\n")
            result = run(root, "status")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("canonical playground", result.stderr)
            self.assertFalse((root / "eval-runs").exists())


if __name__ == "__main__":
    unittest.main()

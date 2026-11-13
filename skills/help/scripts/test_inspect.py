#!/usr/bin/env python3
"""Filesystem checks for the read-only help inventory."""

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inspect as inventory


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt(root, folder, case_hash, counts, complete=True, when=10):
    directory = root / folder
    directory.mkdir(parents=True)
    manifest = {"cases_source": {"path": "evals/cases.jsonl", "sha256": case_hash}, "identity": {"files": {"evals/cases.jsonl": case_hash}}}
    write(directory / "manifest.json", json.dumps(manifest))
    write(directory / "summary.json", json.dumps({"complete": complete, "counts": counts}))
    write(directory / "traces.jsonl", "{}\n")
    os.utime(directory / "summary.json", (when, when))


def campaign(root, folder, case_hash, status="active"):
    directory = root / folder
    directory.mkdir(parents=True)
    write(directory / "contract.json", json.dumps({"identity": {"files": {"evals/cases.jsonl": case_hash}}, "max_case_runs": 48}))
    write(directory / "state.json", json.dumps({"status": status, "attempts": [{"status": "complete"}]}))


class InventoryTests(unittest.TestCase):
    def test_checkout_and_canonical_fixture_recommend_course_without_scanning_pack_history(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root / "plugin.json", json.dumps({"name": "cstack"}))
            write(root / "skills/expert-mode/SKILL.md", "---\nname: expert-mode\n---\n")
            write(root / "fixtures/playground/evaluate.py", "# fixture\n")
            write(root / "evals/huge/manifest.json", "{}")
            report = inventory.inspect(root)
            self.assertEqual(report["workspace_kind"], "cstack-checkout")
            self.assertEqual(report["recommendation"]["skill"], "course")
            self.assertEqual(report["receipts"], [])

    def test_empty_playground_starts_the_course_and_a_saved_checkpoint_resumes_it(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root / "evaluate.py", "")
            write(root / "support_agent.py", "")
            write(root / "exercises/01-expert-mode.md", "# 01\n")
            write(root / ".cstack-source.json", '{"source": "/cstack"}\n')
            write(root / "evals/cases.jsonl", json.dumps({"id": "how-to", "expected": {}}) + "\n")
            write(root / "evals/spec.json", "{}\n")
            report = inventory.inspect(root)
            self.assertEqual(report["recommendation"]["skill"], "course")
            self.assertEqual(report["user_cases"], [])
            case_hash = sha(root / "evals/cases.jsonl")
            receipt(root, "eval-runs/expert-baseline", case_hash, {"PASS": 4, "FAIL": 4, "ERROR": 0, "UNKNOWN": 0})
            write(root / "eval-runs/course/progress/state.json", json.dumps({
                "revision": 2, "stage": "02-distill-me", "completed": ["01-expert-mode"],
                "next_action": "Ask which sentence was theirs."}))
            resumed = inventory.inspect(root)
            self.assertEqual(resumed["recommendation"]["skill"], "course")
            self.assertIn("02-distill-me", resumed["recommendation"]["why"])

    def test_contract_and_receipt_states_pick_one_skill(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root / "README.md", "# product\n")
            cases = write(root / "evals/cases.jsonl", json.dumps({"id": "a", "expected": {"ok": True}}) + "\n")
            only_cases = inventory.inspect(root)
            self.assertEqual(only_cases["recommendation"]["skill"], "run-eval")
            case_hash = sha(cases)
            receipt(root, "eval-runs/baseline", case_hash, {"PASS": 0, "FAIL": 1, "ERROR": 0, "UNKNOWN": 0}, when=10)
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "hill-climb")
            campaign(root, "eval-runs/demo", case_hash, status="active")
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "hill-climb")
            self.assertIn("active", inventory.inspect(root)["recommendation"]["why"])
            write(cases, json.dumps({"id": "a", "expected": {"ok": False}}) + "\n")
            drifted = inventory.inspect(root)
            self.assertEqual(drifted["recommendation"]["skill"], "hill-climb")
            self.assertIn("no longer matches", drifted["recommendation"]["why"])
            (root / "eval-runs/demo/contract.json").unlink()
            (root / "eval-runs/demo/state.json").unlink()
            stale = inventory.inspect(root)
            self.assertEqual(stale["recommendation"]["skill"], "run-eval")
            self.assertTrue(stale["stale"])

    def test_passes_move_from_challenge_to_removal_and_then_capture(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases = write(root / "evals/cases.jsonl", json.dumps({"id": "a", "expected": True}) + "\n")
            case_hash = sha(cases)
            receipt(root, "eval-runs/green", case_hash, {"PASS": 1, "FAIL": 0, "ERROR": 0, "UNKNOWN": 0}, when=20)
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "cross-examine")
            write(root / "eval-runs/audit/CROSS_EXAMINE_LEDGER.md", "Validation: replay accepted the baseline.\n")
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "adversarial-cases")
            write(root / "eval-runs/case-build/notes.md", "challenge\n")
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "ablation")
            write(root / "eval-runs/migration.json", json.dumps({"old_model": "old", "new_model": "new", "complete": False, "missing_cells": ["old/simplified"]}))
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "bitter-lesson")
            write(root / "eval-runs/migration.json", json.dumps({"old_model": "old", "new_model": "new", "complete": True, "selected": "simplified"}))
            write(root / "eval-runs/simplification/state.json", "{}\n")
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "expert-mode")

    def test_records_cases_judges_and_open_reviews_follow_the_order(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root / "README.md", "# product\n")
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "bootstrap")
            write(root / "reviews.jsonl", json.dumps({"example_id": "e1", "unresolved": ["urgency"]}) + "\n")
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "expert-mode")
            write(root / "reviews.jsonl", json.dumps({
                "example_id": "e1", "record_id": "r1", "input": {"q": "how"}, "output": {"action": "create_ticket"},
                "criterion_id": "how-to", "judgment": "creating a ticket is wrong"}) + "\n")
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "create-eval")
            write(root / "config.json", json.dumps({"checks": {"judge": [{"id": "source-named", "question": "Is the source named?"}]}}))
            cases = write(root / "evals/cases.jsonl", json.dumps({"id": "a", "request": "vpn", "expected": True}) + "\n")
            case_hash = sha(cases)
            receipt(root, "eval-runs/scored", case_hash, {"PASS": 1, "FAIL": 0, "ERROR": 0, "UNKNOWN": 0})
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "calibrate-judge")
            write(root / "eval-runs/judge-calibration/results.json", json.dumps({"complete": True}))
            write(root / "eval-runs/bootstrap/handoff.json", json.dumps({"cards": [{"id": "A", "status": "pending"}]}))
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "bootstrap")
            write(root / "eval-runs/audit/LEDGER.md", "status: unreviewed\n")
            self.assertEqual(inventory.inspect(root)["recommendation"]["skill"], "cross-examine")

    def test_unknown_outcomes_are_rerun_and_an_older_stale_receipt_does_not_override_a_newer_match(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases = write(root / "evals/cases.jsonl", json.dumps({"id": "a", "expected": True}) + "\n")
            original = sha(cases)
            receipt(root, "eval-runs/old", original, {"PASS": 1, "FAIL": 0, "ERROR": 0, "UNKNOWN": 0}, when=5)
            write(cases, json.dumps({"id": "a", "expected": False}) + "\n")
            receipt(root, "eval-runs/new", sha(cases), {"PASS": 0, "FAIL": 0, "ERROR": 0, "UNKNOWN": 1}, when=50)
            report = inventory.inspect(root)
            self.assertEqual(report["recommendation"]["skill"], "run-eval")
            self.assertIn("unknown", report["recommendation"]["why"])
            self.assertIn("eval-runs/old", report["stale"])


if __name__ == "__main__":
    unittest.main()

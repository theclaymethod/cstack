"""Behavioral checks use actual standalone candidate subprocesses and temp repos."""

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


PROJECT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("playground_evaluate", PROJECT / "evaluate.py")
evaluate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluate)


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cstack-campaign-test-")
        self.root = Path(self.temp.name)
        shutil.copytree(PROJECT / "evals", self.root / "evals")
        shutil.copyfile(PROJECT / "evaluate.py", self.root / "evaluate.py")
        shutil.copyfile(PROJECT / "support_agent.py", self.root / "support_agent.py")
        shutil.copytree(PROJECT / "examples/candidates", self.root / "candidates")
        self.patch = mock.patch.object(evaluate, "ROOT", self.root)
        self.patch.start()
        self.campaign = self.root / "campaign"
        self.baseline = self.root / "support_agent.py"
        self.improved = self.root / "candidates/improved.py"
        self.regression = self.root / "candidates/regression.py"

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def test_actual_code_changes_outputs_and_regressions_are_not_average_gains(self):
        baseline = evaluate.run_suite(self.baseline, "development", self.root / "baseline")
        improved = evaluate.run_suite(self.improved, "development", self.root / "improved")
        regression = evaluate.run_suite(self.regression, "development", self.root / "regression")
        self.assertEqual([baseline["counts"]["PASS"], improved["counts"]["PASS"], regression["counts"]["PASS"]], [4, 8, 6])
        before = [json.loads(line) for line in (self.root / "baseline/traces.jsonl").read_text().splitlines()]
        after = [json.loads(line) for line in (self.root / "improved/traces.jsonl").read_text().splitlines()]
        self.assertNotEqual(before[0]["output"], after[0]["output"])
        self.assertNotEqual(baseline["candidate_hash"], improved["candidate_hash"])
        bad = evaluate.compare_runs(self.root / "baseline", self.root / "regression")
        self.assertTrue(bad["strict_improvement"])
        self.assertEqual(set(bad["regressions"]), {"dev-closed", "dev-unrelated"})
        self.assertFalse(bad["admissible"])

    def test_ticket_metadata_is_accepted_preserved_and_not_silently_changed(self):
        candidate = self.root / "metadata.py"
        candidate.write_text(
            "import json,runpy,sys\n"
            "respond=runpy.run_path(" + repr(str(self.improved)) + ")[\"respond\"]\n"
            "output=respond(json.load(sys.stdin))\n"
            "if output['action']=='create_ticket':\n"
            " output['state']['tickets'][-1]['created_at']='2026-11-10T00:00:00Z'\n"
            "print(json.dumps(output))\n")
        created = self.root / "metadata-creation"
        summary = evaluate.run_suite(candidate, "development", created)
        self.assertEqual(summary["counts"], {"PASS": 8, "FAIL": 0, "ERROR": 0, "UNKNOWN": 0})
        trace = next(json.loads(line) for line in (created / "traces.jsonl").read_text().splitlines()
                     if json.loads(line)["id"] == "dev-explicit")
        case = copy.deepcopy(next(c for c in evaluate.load_cases("development") if c["id"] == "dev-explicit"))
        case["state"] = trace["output"]["state"]
        case["expected"] = {"allowed_actions": ["guidance", "clarify"], "account": None, "ticket_delta": 0}
        cases = self.root / "metadata-followup.jsonl"
        cases.write_text(json.dumps(case) + "\n")
        followup = evaluate.run_suite(self.improved, "development", self.root / "metadata-followup", cases)
        self.assertEqual(followup["counts"]["PASS"], 1)
        changed = copy.deepcopy(case["state"])
        changed["tickets"][0]["created_at"] = "changed"
        verdict = evaluate.grade({"action": "guidance", "account": None, "state": changed, "note": "Use existing ticket"}, case)
        self.assertEqual(verdict["outcome"], "FAIL")
        self.assertFalse(verdict["checks"]["preserved_tickets"])

    def test_campaign_retains_best_on_no_improvement_regression_and_last_error(self):
        evaluate.start_campaign(self.campaign, 48, 8)
        rejected = evaluate.try_candidate(self.campaign, self.regression, "Check whether duplicate blocking preserves closed tickets")
        self.assertEqual(rejected["decision"], "reject regression")
        self.assertEqual(rejected["best_attempt"], 0)
        unchanged = evaluate.try_candidate(self.campaign, self.baseline, "Unchanged program should not count as improvement")
        self.assertEqual(unchanged["decision"], "no improvement")
        accepted = evaluate.try_candidate(self.campaign, self.improved, "Require authorization and scope duplicate checks")
        self.assertEqual(accepted["decision"], "retain improvement")
        broken = self.root / "broken.py"
        broken.write_text("raise RuntimeError('fixture failure')\n")
        error = evaluate.try_candidate(self.campaign, broken, "Failed execution remains charged and cannot replace best")
        self.assertEqual(error["comparison"]["errors"], 8)
        self.assertEqual(error["best_attempt"], accepted["best_attempt"])
        self.assertEqual(error["used_case_runs"], 40)
        result = evaluate.finish_campaign(self.campaign)
        self.assertEqual(result["used_case_runs"], 48)
        self.assertEqual(evaluate.digest(self.campaign / "best.py"), evaluate.digest(self.improved))
        self.assertTrue((self.campaign / "best.diff").read_text())
        self.assertEqual(result["selection"]["confirmation"]["candidate_score"], 1)
        self.assertEqual(evaluate.finish_campaign(self.campaign)["used_case_runs"], 48)

    def test_confirmation_reserve_blocks_search_and_baseline_is_delivered_without_gain(self):
        evaluate.start_campaign(self.campaign, 16, 8)
        with self.assertRaisesRegex(evaluate.CampaignError, "reserve"):
            evaluate.try_candidate(self.campaign, self.improved, "Cannot spend reserved confirmation")
        self.assertEqual(evaluate.campaign_status(self.campaign)["used_case_runs"], 8)
        result = evaluate.finish_campaign(self.campaign)
        self.assertEqual(result["used_case_runs"], 16)
        self.assertEqual(result["last_decision"], "no verified improvement; baseline retained")
        self.assertEqual(result["selection"]["stop_reason"], "no verified improvement")
        self.assertEqual(evaluate.digest(self.campaign / "best.py"), evaluate.digest(self.baseline))
        self.assertEqual((self.campaign / "best.diff").read_text(), "")

    def test_confirmation_regression_preserves_baseline_despite_development_gain(self):
        candidate = self.root / "confirmation-regression.py"
        code = self.improved.read_text().replace(
            '    account = request["account"]\n',
            '    if request["account"] == "team-south":\n'
            '        return reply("guidance", "Synthetic confirmation-only failure control")\n'
            '    account = request["account"]\n')
        candidate.write_text(code)
        evaluate.start_campaign(self.campaign, 24, 8)
        accepted = evaluate.try_candidate(self.campaign, candidate, "Synthetic control: development gain can still regress in confirmation")
        self.assertEqual(accepted["decision"], "retain improvement")
        finished = evaluate.finish_campaign(self.campaign)
        comparison = finished["selection"]["confirmation"]
        self.assertEqual(comparison["regressions"], ["conf-targeted"])
        self.assertGreater(comparison["candidate_score"], comparison["baseline_score"])
        self.assertFalse(finished["selection"]["confirmation_selected"])
        self.assertEqual(evaluate.digest(self.campaign / "best.py"), evaluate.digest(self.baseline))

    def test_interrupted_confirmation_is_charged_and_not_reused_as_success(self):
        evaluate.start_campaign(self.campaign, 16, 8)
        with mock.patch.object(evaluate, "run_case", side_effect=KeyboardInterrupt()):
            with self.assertRaises(KeyboardInterrupt):
                evaluate.finish_campaign(self.campaign)
        status = evaluate.campaign_status(self.campaign)
        self.assertEqual(status["used_case_runs"], 12)
        self.assertEqual(status["pending_attempts"], [1])
        self.assertFalse((self.campaign / "best.py").exists())
        with self.assertRaisesRegex(evaluate.CampaignError, "confirmation interrupted"):
            evaluate.finish_campaign(self.campaign)
        self.assertEqual(evaluate.campaign_status(self.campaign)["used_case_runs"], 12)

    def test_source_python_and_protocol_drift_refuse_resume(self):
        evaluate.start_campaign(self.campaign)
        for relative in evaluate.FROZEN_FILES:
            path = self.root / relative
            old = path.read_bytes()
            path.write_bytes(old + b"\n")
            with self.assertRaisesRegex(evaluate.CampaignError, "frozen source"):
                evaluate.campaign_status(self.campaign)
            path.write_bytes(old)
        with mock.patch.object(evaluate.platform, "python_implementation", return_value="ChangedPython"):
            with self.assertRaisesRegex(evaluate.CampaignError, "frozen source"):
                evaluate.campaign_status(self.campaign)
        altered = dict(evaluate.PROTOCOL, trials_per_case=2)
        with mock.patch.object(evaluate, "PROTOCOL", altered):
            with self.assertRaisesRegex(evaluate.CampaignError, "frozen source"):
                evaluate.campaign_status(self.campaign)
        self.assertEqual(evaluate.campaign_status(self.campaign)["used_case_runs"], 8)

    def test_interrupted_attempt_is_charged_incomplete_and_not_best(self):
        evaluate.start_campaign(self.campaign, 24, 8)
        real_run_case = evaluate.run_case
        calls = 0

        def interrupt_after_one(*args):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise KeyboardInterrupt()
            return real_run_case(*args)

        with mock.patch.object(evaluate, "run_case", side_effect=interrupt_after_one):
            with self.assertRaises(KeyboardInterrupt):
                evaluate.try_candidate(self.campaign, self.improved, "Interrupt during real execution")
        status = evaluate.campaign_status(self.campaign)
        self.assertEqual(status["used_case_runs"], 16)
        self.assertEqual(status["pending_attempts"], [1])
        self.assertEqual(status["best_attempt"], 0)
        partial = evaluate.read_json(self.campaign / "attempts/001-proposal/summary.json")
        self.assertFalse(partial["complete"])
        self.assertEqual(partial["executed_count"], 1)
        with self.assertRaisesRegex(evaluate.CampaignError, "incomplete"):
            evaluate.compare_runs(self.campaign / "attempts/000-baseline", self.campaign / "attempts/001-proposal")
        with self.assertRaisesRegex(evaluate.CampaignError, "reserve"):
            evaluate.try_candidate(self.campaign, self.improved, "Interrupted budget is not refunded")
        finished = evaluate.finish_campaign(self.campaign)
        self.assertEqual(finished["used_case_runs"], 24)
        self.assertEqual(evaluate.digest(self.campaign / "best.py"), evaluate.digest(self.baseline))

    def test_interrupted_decision_recovers_measured_winner_without_spending_again(self):
        evaluate.start_campaign(self.campaign, 24, 8)
        with mock.patch.object(evaluate, "compare_runs", side_effect=KeyboardInterrupt()):
            with self.assertRaises(KeyboardInterrupt):
                evaluate.try_candidate(self.campaign, self.improved, "Measured winner must survive an interrupted decision")
        saved = evaluate.read_json(self.campaign / "state.json")
        self.assertEqual(saved["attempts"][1]["status"], "complete")
        self.assertNotIn("decision", saved["attempts"][1])
        receipts = saved["attempts"][1]["evidence_hashes"]
        with mock.patch.object(evaluate, "run_case", side_effect=AssertionError("recovery must not execute product")):
            recovered = evaluate.campaign_status(self.campaign)
            self.assertEqual(recovered["used_case_runs"], 16)
            self.assertEqual(recovered["best_attempt"], 1)
            self.assertEqual(recovered["pending_attempts"], [])
            self.assertEqual(evaluate.campaign_status(self.campaign)["best_attempt"], 1)
        saved = evaluate.read_json(self.campaign / "state.json")
        self.assertTrue(saved["attempts"][1]["decision_recovered"])
        self.assertEqual(saved["attempts"][1]["evidence_hashes"], receipts)
        self.assertEqual(saved["attempts"][1]["decision"], "retain improvement")
        finished = evaluate.finish_campaign(self.campaign)
        self.assertEqual(finished["used_case_runs"], 24)
        self.assertEqual(evaluate.digest(self.campaign / "best.py"), evaluate.digest(self.improved))

    def test_custom_cases_execute_native_grader_and_compare_rejects_changed_semantics(self):
        cases = evaluate.load_cases("development")[:1]
        custom = self.root / "authored.jsonl"
        custom.write_text(json.dumps(cases[0]) + "\n")
        result = evaluate.run_suite(self.improved, "development", self.root / "authored-run", custom)
        self.assertEqual(result["counts"]["PASS"], 1)
        self.assertEqual(result["case_ids"], [cases[0]["id"]])
        manifest = evaluate.read_json(self.root / "authored-run/manifest.json")
        self.assertEqual(manifest["cases_source"]["sha256"], evaluate.digest(custom))
        # Same ID and label do not excuse changed request/context semantics.
        cases[0]["request"]["text"] = "New wording, same expected action"
        custom.write_text(json.dumps(cases[0]) + "\n")
        evaluate.run_suite(self.improved, "development", self.root / "changed-run", custom)
        with self.assertRaisesRegex(evaluate.CampaignError, "different evaluation"):
            evaluate.compare_runs(self.root / "authored-run", self.root / "changed-run")

    def test_grader_requires_exact_state_preservation_and_creation_fields(self):
        case = next(c for c in evaluate.load_cases("all") if c["id"] == "conf-preservation")
        good = evaluate.run_case(self.improved, case)["output"]
        self.assertEqual(evaluate.grade(good, case)["outcome"], "PASS")
        mutations = []
        wrong = copy.deepcopy(good)
        wrong["state"]["tickets"][0]["status"] = "closed" if wrong["state"]["tickets"][0]["status"] == "open" else "open"
        mutations.append(wrong)
        wrong = copy.deepcopy(good)
        wrong["state"]["tickets"][:2] = list(reversed(wrong["state"]["tickets"][:2]))
        mutations.append(wrong)
        for field, value in (("id", good["state"]["tickets"][0]["id"]), ("account", "unauthorized"), ("status", "closed"), ("issue", "password")):
            wrong = copy.deepcopy(good)
            wrong["state"]["tickets"][-1][field] = value
            mutations.append(wrong)
        wrong = copy.deepcopy(good)
        wrong["state"]["new-secret-field"] = True
        mutations.append(wrong)
        for mutated in mutations:
            with self.subTest(mutated=mutated):
                self.assertEqual(evaluate.grade(mutated, case)["outcome"], "FAIL")
        self.assertEqual(evaluate.grade({"action": "guidance"}, case)["outcome"], "ERROR")

    def test_snapshot_and_evidence_tampering_are_detected(self):
        evaluate.start_campaign(self.campaign)
        snapshot = self.campaign / "attempts/000-baseline/candidate.py"
        snapshot.chmod(0o644)
        snapshot.write_text(snapshot.read_text() + "\n# modified\n")
        with self.assertRaisesRegex(evaluate.CampaignError, "evidence changed"):
            evaluate.campaign_status(self.campaign)

    def test_standalone_comparison_rejects_summary_and_trace_verdict_forgery(self):
        evaluate.run_suite(self.baseline, "development", self.root / "baseline")
        evaluate.run_suite(self.regression, "development", self.root / "regression")
        result_path = self.root / "regression/summary.json"
        original = result_path.read_text()
        forged = json.loads(original)
        for result in forged["results"]:
            result["outcome"] = "PASS"
        forged["counts"] = {"PASS": 8, "FAIL": 0, "ERROR": 0, "UNKNOWN": 0}
        forged["score"] = 1
        evaluate.write_json(result_path, forged)
        with self.assertRaisesRegex(evaluate.CampaignError, "summary differs from execution trace"):
            evaluate.compare_runs(self.root / "baseline", self.root / "regression")
        # Faking both reported verdicts still cannot change retained outputs.
        trace_path = self.root / "regression/traces.jsonl"
        traces = [json.loads(line) for line in trace_path.read_text().splitlines()]
        for trace, result in zip(traces, forged["results"]):
            trace["outcome"] = "PASS"
            trace["checks"] = {key: True for key in trace["checks"]}
            result["checks"] = trace["checks"]
        trace_path.write_text("".join(json.dumps(trace) + "\n" for trace in traces))
        evaluate.write_json(result_path, forged)
        with self.assertRaisesRegex(evaluate.CampaignError, "trace verdict differs"):
            evaluate.compare_runs(self.root / "baseline", self.root / "regression")

    def test_exact_preservation_distinguishes_nested_json_types_and_allows_key_order(self):
        case = copy.deepcopy(evaluate.load_cases("development")[0])
        case["state"]["metadata"] = {"a": {"value": 1, "flag": False}, "b": [1, {"count": 1}]}
        good = evaluate.run_case(self.improved, case)["output"]
        good["state"]["metadata"] = {"b": [1, {"count": 1}], "a": {"flag": False, "value": 1}}
        self.assertEqual(evaluate.grade(good, case)["outcome"], "PASS")
        for branch in ("a", "b"):
            wrong = copy.deepcopy(good)
            if branch == "a":
                wrong["state"]["metadata"]["a"]["value"] = True
            else:
                wrong["state"]["metadata"]["b"][1]["count"] = True
            result = evaluate.grade(wrong, case)
            self.assertEqual(result["outcome"], "FAIL")
            self.assertFalse(result["checks"]["preserved_other_state"])

    def test_malformed_authored_cases_are_setup_errors_before_candidate_execution(self):
        original = evaluate.load_cases("development")[0]
        mutations = []
        for field in ("text", "account", "accounts"):
            wrong = copy.deepcopy(original)
            del wrong["request"][field]
            mutations.append(wrong)
        for field, value in (("id", None), ("request", []), ("state", []), ("expected", [])):
            wrong = copy.deepcopy(original)
            wrong[field] = value
            mutations.append(wrong)
        wrong = copy.deepcopy(original)
        wrong["expected"]["allowed_actions"] = "guidance"
        mutations.append(wrong)
        wrong = copy.deepcopy(original)
        wrong["expected"]["account"] = True
        mutations.append(wrong)
        for index, wrong in enumerate(mutations):
            source = self.root / f"invalid-{index}.jsonl"
            source.write_text(json.dumps(wrong) + "\n")
            out = self.root / f"invalid-run-{index}"
            with self.subTest(index=index), mock.patch.object(evaluate, "run_case") as execute:
                with self.assertRaises(evaluate.CampaignError):
                    evaluate.run_suite(self.improved, "all", out, source)
                execute.assert_not_called()
                self.assertFalse(out.exists())

    def test_cli_custom_cases_and_malformed_outputs_report_errors(self):
        malformed = self.root / "malformed.py"
        malformed.write_text("print('not JSON')\n")
        custom = self.root / "one-case.jsonl"
        custom.write_text(json.dumps(evaluate.load_cases("development")[0]) + "\n")
        process = subprocess.run([sys.executable, str(self.root / "evaluate.py"), "run", "--candidate", str(malformed),
                                  "--suite", "all", "--cases", str(custom), "--out", str(self.root / "cli-run")],
                                 capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        summary = json.loads(process.stdout)
        self.assertEqual(summary["counts"], {"PASS": 0, "FAIL": 0, "ERROR": 1, "UNKNOWN": 0})
        self.assertEqual(summary["selected_count"], 1)
        self.assertEqual(summary["score"], 0)

    def test_declared_output_schema_cannot_earn_selection(self):
        source = self.improved.read_text()
        for name, replacement in [("empty", '"note": ""}'),
                                  ("extra", '"note": note, "undeclared": True}'),
                                  ("combined", '"note": "", "undeclared": True}')]:
            candidate = self.root / (name + '.py')
            candidate.write_text(source.replace('"note": note}', replacement))
            result = evaluate.run_suite(candidate, 'all', self.root / (name + '-run'))
            self.assertEqual(result['counts']['ERROR'], 12)
            self.assertEqual(result['counts']['PASS'], 0)
        evaluate.start_campaign(self.campaign, 24, 8)
        decision = evaluate.try_candidate(self.campaign, self.root / 'combined.py', 'Schema errors cannot earn promotion')
        self.assertEqual(decision['best_attempt'], 0)
        selected = evaluate.finish_campaign(self.campaign)
        self.assertEqual(selected['selection']['selected_attempt'], 0)
        valid = self.root / 'alternative.py'
        valid.write_text(source.replace('ticket-{sequence}', 'alternate-{sequence}')
                         .replace('"note": note}', '"note": "An alternative explanation."}'))
        result = evaluate.run_suite(valid, 'all', self.root / 'alternative-run')
        self.assertEqual(result['counts']['PASS'], 12)

    def test_fully_measured_baseline_recovers_without_new_execution(self):
        real_run = evaluate.run_suite
        def interrupted(*args, **kwargs):
            real_run(*args, **kwargs)
            raise KeyboardInterrupt()
        with mock.patch.object(evaluate, 'run_suite', side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt):
                evaluate.start_campaign(self.campaign, 16, 8)
        with mock.patch.object(evaluate, 'run_case', side_effect=AssertionError('Recovery must not execute')):
            status = evaluate.campaign_status(self.campaign)
        self.assertEqual(status['used_case_runs'], 8)
        self.assertEqual(status['best_attempt'], 0)
        self.assertEqual(status['pending_attempts'], [])
        self.assertTrue(evaluate.read_json(self.campaign / 'state.json')['attempts'][0]['completion_recovered'])

    def test_fully_measured_proposal_recovers_and_is_selected_without_recharge(self):
        evaluate.start_campaign(self.campaign, 24, 8)
        real_run = evaluate.run_suite
        def interrupted(*args, **kwargs):
            real_run(*args, **kwargs)
            raise KeyboardInterrupt()
        with mock.patch.object(evaluate, 'run_suite', side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt):
                evaluate.try_candidate(self.campaign, self.improved, 'Complete measurement before receipt commit')
        before = evaluate.digest(self.campaign / 'attempts/001-proposal/traces.jsonl')
        with mock.patch.object(evaluate, 'run_case', side_effect=AssertionError('Recovery must not execute')):
            status = evaluate.campaign_status(self.campaign)
        self.assertEqual(status['used_case_runs'], 16)
        self.assertEqual(status['best_attempt'], 1)
        self.assertEqual(status['pending_attempts'], [])
        self.assertEqual(evaluate.digest(self.campaign / 'attempts/001-proposal/traces.jsonl'), before)
        selected = evaluate.finish_campaign(self.campaign)
        self.assertEqual(selected['used_case_runs'], 24)
        self.assertEqual(selected['selection']['selected_attempt'], 1)
        self.assertEqual(evaluate.digest(self.campaign / 'best.py'), evaluate.digest(self.improved))

    def test_complete_confirmation_receipts_recover_without_duplicate_spend(self):
        real_run = evaluate.run_suite
        for phase in ['confirm-baseline', 'confirm-incumbent']:
            campaign = self.root / phase
            evaluate.start_campaign(campaign, 24, 8)
            evaluate.try_candidate(campaign, self.improved, 'Confirm the measured improvement')
            def interrupted(candidate, suite, out, cases_file=None):
                result = real_run(candidate, suite, out, cases_file)
                if Path(out).name.endswith(phase):
                    raise KeyboardInterrupt()
                return result
            with mock.patch.object(evaluate, 'run_suite', side_effect=interrupted):
                with self.assertRaises(KeyboardInterrupt):
                    evaluate.finish_campaign(campaign)
            spent = evaluate.read_json(campaign / 'state.json')['used_case_runs']
            with mock.patch.object(evaluate, 'run_case', side_effect=AssertionError('Recovery must not execute')):
                status = evaluate.campaign_status(campaign)
            self.assertEqual(status['used_case_runs'], spent)
            self.assertEqual(status['pending_attempts'], [])
            selected = evaluate.finish_campaign(campaign)
            self.assertEqual(selected['used_case_runs'], 24)
            self.assertEqual(selected['selection']['selected_attempt'], 1)

    def test_invalid_complete_evidence_remains_pending_and_charged(self):
        evaluate.start_campaign(self.campaign, 24, 8)
        real_run = evaluate.run_suite
        def interrupted(*args, **kwargs):
            real_run(*args, **kwargs)
            raise KeyboardInterrupt()
        with mock.patch.object(evaluate, 'run_suite', side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt):
                evaluate.try_candidate(self.campaign, self.improved, 'Receipt validation is required')
        summary_path = self.campaign / 'attempts/001-proposal/summary.json'
        summary = evaluate.read_json(summary_path)
        summary['candidate_hash'] = 'does-not-match-the-reserved-candidate'
        evaluate.write_json(summary_path, summary)
        with mock.patch.object(evaluate, 'run_case', side_effect=AssertionError('Invalid evidence must not execute')):
            status = evaluate.campaign_status(self.campaign)
        self.assertEqual(status['best_attempt'], 0)
        self.assertEqual(status['used_case_runs'], 16)
        self.assertEqual(status['pending_attempts'], [1])


if __name__ == "__main__":
    unittest.main()

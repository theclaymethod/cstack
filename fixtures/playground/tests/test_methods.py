"""Observable method outcomes, native controls, provenance and actual optional DSPy SDK."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from methods import synthetic, faults, dspy_handoff
from methods.native import ROOT, Runs, evaluate, read_rows


class GenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='cstack-method-data-')
        cls.root = Path(cls.temp.name)
        cls.results = synthetic.run(cls.root / 'generated')
        cls.records = read_rows(cls.root / 'generated/records.jsonl')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_reachable_sequence_adds_declared_fault_detection_beyond_seeds(self):
        self.assertEqual(self.results['matrix']['ignore-own-created']['seed_failures'], [])
        steps = self.results['sequence_results']['ignore-own-created']
        self.assertEqual([s['trace']['outcome'] for s in steps], ['PASS', 'FAIL'])
        self.assertEqual(steps[1]['case']['state'], steps[0]['trace']['output']['state'])
        self.assertTrue(steps[1]['trace']['checks']['preserved_tickets'])
        self.assertFalse(steps[1]['trace']['checks']['ticket_delta'])
        self.assertEqual([s['trace']['outcome'] for s in self.results['sequence_results']['conforming']], ['PASS', 'PASS'])
        actual = sum(len(read_rows(p)) for p in (self.root / 'generated/native').glob('*/traces.jsonl'))
        self.assertEqual(actual, self.results['actual_native_executions'])
        self.assertLessEqual(actual, self.results['budget'])
        originals = {evaluate.json_hash({'request': c['request'], 'state': c['state']}): c
                     for c in evaluate.load_cases('all')}
        for row in self.records:
            matching = originals.get(row['metadata']['input_hash'])
            if matching:
                self.assertEqual(row['case']['expected'], matching['expected'])

    def test_reduction_preserves_mechanism_controls_and_rejected_attempt(self):
        reductions = self.results['reduction']['attempts']
        self.assertEqual([r['retained'] for r in reductions], [True, True, True, False])
        for row in reductions[:-1]:
            self.assertEqual([s['trace']['outcome'] for s in row['legitimate_controls']], ['PASS', 'PASS'])
        self.assertEqual(reductions[-1]['step']['trace']['outcome'], 'PASS')
        self.assertFalse(self.results['reduction']['global_minimality_claimed'])
        self.assertEqual(self.results['surviving_mutants'], [])
        for detected in self.results['complete_detection_matrix'].values():
            self.assertTrue(set(detected) & set(self.results['selected_case_ids']))

    def test_connected_ancestry_and_identical_inputs_never_cross_partitions(self):
        records = copy.deepcopy(self.records[:4])
        records[0]['metadata']['ancestors'] = ['a']
        records[1]['metadata']['ancestors'] = ['a', 'b']
        records[2]['metadata']['ancestors'] = ['b']
        records[3]['metadata']['ancestors'] = ['independent']
        for i, row in enumerate(records): row['case']['family'] = 'separate-' + str(i)
        result = synthetic.partition(records)
        membership = {row['case']['id']: name for name, rows in result.items() for row in rows}
        self.assertEqual(len({membership[row['case']['id']] for row in records[:3]}), 1)
        self.assertNotEqual(membership[records[0]['case']['id']], membership[records[3]['case']['id']])

    def test_export_rejects_proposals_stale_expectations_and_changed_inputs(self):
        for kind in ['proposal', 'expectation', 'input']:
            rows = copy.deepcopy(self.records)
            if kind == 'proposal': rows[0]['metadata']['label_status'] = 'pending'
            elif kind == 'expectation': rows[0]['case']['expected']['ticket_delta'] = 0
            else: rows[0]['case']['request']['accounts'] = ['other']
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                dspy_handoff.validate_records(rows)

    def test_duplicate_run_label_preserves_case_source_ledger_and_budget(self):
        runs = Runs(self.root / 'duplicate-guard', 2)
        cases = [synthetic.case_for('guard:create', 'create')]
        runs.run('original', ROOT / 'examples/candidates/improved.py', cases)
        case_bytes = (runs.directory / 'original.jsonl').read_bytes()
        ledger_bytes = (runs.directory / 'executions.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'unused'):
            runs.run('original', ROOT / 'examples/candidates/improved.py',
                     [synthetic.case_for('guard:deny', 'deny')])
        self.assertEqual((runs.directory / 'original.jsonl').read_bytes(), case_bytes)
        self.assertEqual((runs.directory / 'executions.json').read_bytes(), ledger_bytes)
        self.assertEqual(runs.reserved, 1)
        self.assertEqual(len(runs.calls), 1)

    @unittest.skipUnless(importlib.util.find_spec('dspy'), 'Optional DSPy SDK not installed')
    def test_actual_dspy_examples_evaluate_feedback_and_no_label_inputs(self):
        output = self.root / 'export'
        dspy_handoff.export(self.root / 'generated/records.jsonl', output)
        result = dspy_handoff.smoke(output, self.root / 'sdk-check')
        self.assertEqual(result['evaluate_percentage'], 100)
        self.assertEqual(result['false_claim']['outcome'], 'FAIL')
        self.assertEqual(result['malformed']['outcome'], 'ERROR')
        self.assertEqual(result['execution_error']['outcome'], 'ERROR')
        self.assertEqual(result['provider_calls'], 0)
        # A changed exported file cannot silently become new optimization evidence.
        path = output / 'train.jsonl'; path.write_text(path.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'changed'):
            dspy_handoff.load(output)


class FaultTests(unittest.TestCase):
    def test_actual_boundaries_errors_storage_retry_and_nonactivation(self):
        with tempfile.TemporaryDirectory(prefix='cstack-method-fault-') as temp:
            result = faults.run(Path(temp) / 'faults')
            self.assertEqual(result['process_interruptions'], 3)
            self.assertEqual(result['actual_native_executions'], 45)
            by_name = {row['label']: row for row in result['lifecycle']}
            self.assertEqual(by_name['armed-unreached']['activation_count'], 0)
            self.assertEqual(by_name['observed-noop']['activation_count'], 1)
            self.assertEqual(by_name['reservation']['after']['attempts'][0]['status'], 'pending')
            self.assertIsNone(by_name['reservation']['after']['best_attempt'])
            for name in ['summary', 'completion']:
                self.assertEqual(by_name[name]['process']['exit'], -9)
                self.assertEqual(by_name[name]['after']['best_attempt'], 0)
            for row in result['storage']:
                self.assertEqual(len(row['events']), {'noop': 0, 'once': 1, 'persistent': 2}[row['action']])
            self.assertEqual([row['outcome'] for row in result['subprocess']], ['PASS', 'ERROR', 'ERROR', 'ERROR', 'ERROR'])
            self.assertEqual(result['subprocess'][3]['exit_code'], 2)
            self.assertEqual(json.loads(result['subprocess'][3]['stdout'])['action'], 'create_ticket')
            self.assertIsNone(result['subprocess'][3]['output'])


if __name__ == '__main__':
    unittest.main()

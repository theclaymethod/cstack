"""Observe removal interactions, original-baseline gates and closed final work."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from simplification.protocol import Experiment, UNITS, configuration, quality_gate
from methods.native import evaluate


FULL = set(UNITS)
LEAN = {'contract', 'legacy-auth', 'duplicate-b'}


class SimplificationTests(unittest.TestCase):
    def test_protected_units_dependencies_and_configuration_are_validated(self):
        for retained in [FULL - {'contract'}, FULL - {'plan'}, ['contract', 'contract'],
                         ['contract', 'unknown'], [True], 'contract']:
            with self.assertRaises(ValueError):
                configuration('old-fixture', retained)
        with self.assertRaises(ValueError):
            configuration('real-provider', FULL)
        self.assertEqual(configuration('new-fixture', LEAN)['retained'], sorted(LEAN))

    def test_separately_safe_removals_can_fail_in_combination(self):
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run', limit=32, confirmation_reserve=0)
            for label, retained in [('original', FULL), ('no-a', FULL - {'duplicate-a'}),
                                    ('no-b', FULL - {'duplicate-b'}),
                                    ('no-both', FULL - {'duplicate-a', 'duplicate-b'})]:
                experiment.measure(label, configuration('old-fixture', retained))
            self.assertTrue(experiment.compare('original', 'no-a')['admissible'])
            self.assertTrue(experiment.compare('original', 'no-b')['admissible'])
            result = experiment.compare('original', 'no-both')
            self.assertFalse(result['admissible'])
            self.assertIn('dev-duplicate', result['regressions'])
            self.assertEqual(experiment.runs.reserved, 32)

    def test_group_removal_can_work_when_single_removal_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run', limit=24, confirmation_reserve=0)
            experiment.measure('original', configuration('old-fixture', FULL))
            experiment.measure('one', configuration('old-fixture', FULL - {'conflict-a'}))
            experiment.measure('both', configuration('old-fixture', FULL - {'conflict-a', 'conflict-b'}))
            self.assertFalse(experiment.compare('original', 'one')['admissible'])
            self.assertTrue(experiment.compare('original', 'both')['admissible'])

    def test_loss_is_against_original_and_errors_are_visible(self):
        original = {'outcomes': {str(n): 'PASS' for n in range(10)}}
        first = {'outcomes': dict(original['outcomes'], **{'0': 'FAIL'})}
        second = {'outcomes': dict(first['outcomes'], **{'1': 'FAIL'})}
        self.assertTrue(quality_gate(original, first, .15, True)['admissible'])
        self.assertTrue(quality_gate(first, second, .15, True)['admissible'])
        self.assertFalse(quality_gate(original, second, .15, True)['admissible'])
        error = {'outcomes': {'a': 'ERROR'}}
        result = quality_gate({'outcomes': {'a': 'FAIL'}}, error, 1, True)
        self.assertFalse(result['admissible'])
        self.assertEqual(result['errors_or_unknown'], 1)
        for margin in [True, float('nan'), float('inf'), -1, 10**400]:
            with self.assertRaises(ValueError):
                quality_gate(original, first, margin)
        with self.assertRaises(ValueError):
            quality_gate(original, {'outcomes': {'wrong': 'PASS'}})

    def test_reservation_precedes_execution_and_protects_confirmation(self):
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run', limit=12, confirmation_reserve=8)
            with self.assertRaises(RuntimeError):
                experiment.measure('too-large', configuration('old-fixture', FULL))
            self.assertEqual(experiment.runs.reserved, 0)
            self.assertEqual(experiment.records, {})
            with self.assertRaises(RuntimeError):
                experiment.freeze({str(i): configuration('old-fixture', FULL) for i in range(3)})
            with self.assertRaises(ValueError):
                Experiment(Path(temp) / 'bad', limit=True)

    def test_exact_final_membership_closes_fitting_and_requires_completion(self):
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run', limit=24, confirmation_reserve=8)
            experiment.measure('original', configuration('old-fixture', FULL))
            experiment.measure('reduced', configuration('old-fixture', LEAN))
            experiment.freeze({'final-original': configuration('old-fixture', FULL),
                               'final-reduced': configuration('old-fixture', LEAN)})
            with self.assertRaises(ValueError):
                experiment.measure('late-edit', configuration('old-fixture', LEAN))
            with self.assertRaises(ValueError):
                experiment.confirm('unplanned')
            experiment.confirm('final-original')
            with self.assertRaises(ValueError):
                experiment.finish()
            with self.assertRaises(ValueError):
                experiment.confirm('final-original')
            experiment.confirm('final-reduced')
            experiment.finish()
            self.assertTrue(experiment.compare('final-original', 'final-reduced')['admissible'])
            self.assertEqual(experiment.runs.reserved, 24)
            with self.assertRaises(ValueError):
                experiment.measure('after-final', configuration('old-fixture', LEAN))
            with self.assertRaises(FileExistsError):
                Experiment(Path(temp) / 'run')

    def test_same_simplified_prompt_has_different_simulated_model_behavior(self):
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run', limit=16, confirmation_reserve=0)
            retained = LEAN - {'legacy-auth'}
            old = experiment.measure('old', configuration('old-fixture', retained))
            new = experiment.measure('new', configuration('new-fixture', retained))
            self.assertEqual(old['prompt_utf8_bytes'], new['prompt_utf8_bytes'])
            self.assertLess(sum(v == 'PASS' for v in old['outcomes'].values()), 8)
            self.assertTrue(all(v == 'PASS' for v in new['outcomes'].values()))

    def test_frozen_configuration_cannot_be_changed_through_live_state(self):
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run', limit=4, confirmation_reserve=4)
            plan = {'final': configuration('old-fixture', FULL)}
            experiment.freeze(plan)
            plan['final'] = configuration('new-fixture', {'contract', 'duplicate-b'})
            self.assertEqual(experiment.plan['final']['model'], 'old-fixture')
            experiment.plan['final'] = plan['final']
            with self.assertRaisesRegex(ValueError, 'contract, state, or source changed'):
                experiment.confirm('final')
            self.assertEqual(experiment.runs.reserved, 0)

    def test_completed_evidence_and_contract_tampering_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run', limit=16, confirmation_reserve=0)
            experiment.measure('original', configuration('old-fixture', FULL))
            traces = experiment.runs.directory / 'original' / 'traces.jsonl'
            traces.write_text(traces.read_text() + '\n')
            with self.assertRaisesRegex(ValueError, 'evidence changed'):
                experiment.checked('original')
            self.assertEqual(experiment.runs.reserved, 8)
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run')
            (experiment.directory / 'contract.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'contract, state, or source changed'):
                experiment.measure('original', configuration('old-fixture', FULL))
            self.assertEqual(experiment.runs.reserved, 0)

    def test_interrupted_attempt_stays_charged_and_cannot_freeze(self):
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run', limit=16, confirmation_reserve=8)
            with patch.object(evaluate, 'run_suite', side_effect=RuntimeError('Injected pre-result interruption')):
                with self.assertRaises(RuntimeError):
                    experiment.measure('interrupted', configuration('old-fixture', FULL))
            ledger = json.loads((experiment.runs.directory / 'executions.json').read_text())
            self.assertEqual(ledger['reserved'], 8)
            self.assertEqual(ledger['calls'][0]['status'], 'pending')
            with self.assertRaises(ValueError):
                experiment.freeze({'final': configuration('old-fixture', FULL)})
            with self.assertRaises(RuntimeError):
                experiment.measure('retry', configuration('old-fixture', FULL))
            self.assertEqual(experiment.runs.reserved, 8)

    def test_durable_execution_ledger_must_match_reserved_attempts(self):
        with tempfile.TemporaryDirectory() as temp:
            experiment = Experiment(Path(temp) / 'run', limit=16, confirmation_reserve=0)
            experiment.measure('original', configuration('old-fixture', FULL))
            path = experiment.runs.directory / 'executions.json'
            original = path.read_bytes()
            receipt = json.loads(original)
            for field, replacement in [('reserved', 0), ('actual_completed', 0), ('calls', []), ('limit', 0)]:
                changed = dict(receipt, **{field: replacement})
                path.write_text(json.dumps(changed))
                with self.assertRaisesRegex(ValueError, 'ledger differs'):
                    experiment.checked('original')
                self.assertEqual(experiment.runs.reserved, 8)
                path.write_bytes(original)
            path.unlink()
            with self.assertRaisesRegex(ValueError, 'ledger differs'):
                experiment.checked('original')
            path.write_bytes(original)
            self.assertEqual(experiment.checked('original')['status'], 'complete')


if __name__ == '__main__':
    unittest.main()

"""Exercise actual fixture materialization and preserve canonical/user work."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]


class WorkspaceTests(unittest.TestCase):
    def test_materialized_workspace_has_current_skills_and_executes_candidate(self):
        with tempfile.TemporaryDirectory(prefix='cstack-workspace-') as temp:
            workspace = Path(temp) / 'trial'
            command = [sys.executable, str(PROJECT / 'scripts/new_workspace.py'), '--out', str(workspace)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = json.loads(result.stdout)
            source = Path(receipt['source'])
            expected = {p.parent.name for p in (source / 'skills').glob('*/SKILL.md')}
            self.assertEqual(set(receipt['skills']), expected)
            self.assertIn('adversarial-cases', receipt['skills'])
            self.assertIn('calibrate-judge', receipt['skills'])
            self.assertTrue((workspace / '.git').is_dir())
            for name in receipt['skills']:
                for agent in ['.claude', '.cursor']:
                    self.assertEqual((workspace / agent / 'skills' / name).resolve(),
                                     (workspace / '.agents/skills' / name).resolve())
            checked = subprocess.run([sys.executable, 'scripts/sync_skills.py', '--check'], cwd=workspace,
                                     capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            run = subprocess.run([sys.executable, 'evaluate.py', 'run', '--candidate', 'support_agent.py',
                                  '--suite', 'development', '--out', str(Path(temp) / 'baseline')],
                                 cwd=workspace, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['counts'], {'PASS': 4, 'FAIL': 4, 'ERROR': 0, 'UNKNOWN': 0})
            environment = workspace / '.venv'
            environment.mkdir()
            (environment / 'local-sdk.txt').write_text('Project-local dependency, not fixture source')
            second = Path(temp) / 'without-environment'
            copied = subprocess.run([sys.executable, 'scripts/new_workspace.py', '--out', str(second)],
                                    cwd=workspace, capture_output=True, text=True)
            self.assertEqual(copied.returncode, 0, copied.stderr)
            self.assertFalse((second / '.venv').exists())
            self.assertEqual((environment / 'local-sdk.txt').read_text(), 'Project-local dependency, not fixture source')
            sentinel = workspace / 'keep.txt'
            sentinel.write_text('user work')
            repeated = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(repeated.returncode, 0)
            self.assertEqual(sentinel.read_text(), 'user work')

    def test_refuses_recursive_fixture_output(self):
        nested = PROJECT / 'eval-runs' / 'recursive-materialization-test'
        self.assertFalse(nested.exists())
        result = subprocess.run([sys.executable, str(PROJECT / 'scripts/new_workspace.py'), '--out', str(nested)],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(nested.exists())


if __name__ == '__main__':
    unittest.main()

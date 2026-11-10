"""Replay recorded Hill Climb schema and crash-recovery mechanisms in copies."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'fixtures/playground'
EVIDENCE = Path(__file__).resolve().parent / 'evidence/cross-examine'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.out:
        output = args.out.resolve()
        if output == FIXTURE or FIXTURE in output.parents:
            raise SystemExit('Audit outputs must be outside the canonical fixture')
        output.mkdir(parents=True, exist_ok=False)
    else:
        runs = ROOT / 'eval-runs'
        runs.mkdir(exist_ok=True)
        output = Path(tempfile.mkdtemp(prefix='hill-climb-audit-', dir=runs))
    records = []
    results = {}

    def setup(revision, name):
        project = output / revision / name
        shutil.copytree(FIXTURE, project, ignore=shutil.ignore_patterns('.git', '.agents', '.claude', '.cursor',
                                                                      '__pycache__', 'eval-runs', '*.pyc'))
        if revision == 'original':
            shutil.copy2(EVIDENCE / 'original-evaluate.py', project / 'evaluate.py')
        return project

    def native(project, *argv, stop_role=None):
        runner = project / 'evaluate.py'
        cmd = [sys.executable, str(runner), *map(str, argv)]
        if stop_role:
            cmd = [sys.executable, str(EVIDENCE / 'interrupt_cli.py'), str(runner), stop_role, *map(str, argv)]
        process = subprocess.run(cmd, capture_output=True, text=True)
        records.append({'command': cmd, 'exit': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr,
                        'runner_sha256': digest(runner)})
        (output / 'commands.json').write_text(json.dumps(records, indent=2) + '\n')
        if stop_role:
            assert process.returncode == 99, records[-1]
            return None
        if process.returncode != 0:
            return {'exit': process.returncode, 'stderr': process.stderr}
        return json.loads(process.stdout)

    def snapshots(campaign):
        return {str(p.relative_to(campaign)): digest(p) for p in (campaign / 'attempts').rglob('*') if p.is_file()}

    for revision in ['original', 'repaired']:
        project = setup(revision, 'schema')
        source = (project / 'examples/candidates/improved.py').read_text()
        good = native(project, 'run', '--candidate', project / 'examples/candidates/improved.py', '--suite', 'all', '--out', project / 'eval-runs/valid')
        assert good['counts']['PASS'] == 12
        invalid = {}
        for name, replacement in [('empty-note', '"note": ""}'), ('extra-key', '"note": note, "undeclared": True}')]:
            candidate = project / (name + '.py')
            candidate.write_text(source.replace('"note": note}', replacement))
            invalid[name] = native(project, 'run', '--candidate', candidate, '--suite', 'all', '--out', project / 'eval-runs' / name)['counts']
            assert invalid[name]['PASS' if revision == 'original' else 'ERROR'] == 12
        candidate = project / 'combined.py'
        candidate.write_text(source.replace('"note": note}', '"note": "", "undeclared": True}'))
        campaign = project / 'eval-runs/campaign'
        native(project, 'start', '--campaign', campaign, '--max-case-runs', 24, '--reserve-case-runs', 8)
        proposal = native(project, 'try', '--campaign', campaign, '--candidate', candidate, '--hypothesis', 'Declared schema is part of the output contract')
        selected = native(project, 'finish', '--campaign', campaign)
        assert selected['selection']['selected_attempt'] == (1 if revision == 'original' else 0)
        results[revision] = {'schema': {'invalid': invalid, 'decision': proposal['decision'], 'selected_attempt': selected['selection']['selected_attempt']}}

        for role in ['proposal', 'confirm-incumbent']:
            project = setup(revision, role)
            campaign = project / 'eval-runs/campaign'
            native(project, 'start', '--campaign', campaign, '--max-case-runs', 24, '--reserve-case-runs', 8)
            native(project, 'try', '--campaign', campaign, '--candidate', project / 'examples/candidates/improved.py',
                   '--hypothesis', 'Recover completed native evidence', stop_role='proposal' if role == 'proposal' else None)
            if role == 'confirm-incumbent':
                native(project, 'finish', '--campaign', campaign, stop_role=role)
            before = snapshots(campaign)
            status = native(project, 'verify', '--campaign', campaign)
            assert before == snapshots(campaign), 'Recovery must preserve evidence and avoid new execution'
            assert status['used_case_runs'] == (16 if role == 'proposal' else 24)
            if revision == 'original':
                assert status['pending_attempts']
            else:
                assert not status['pending_attempts'] and status['best_attempt'] == 1
            final = native(project, 'finish', '--campaign', campaign)
            if revision == 'original' and role == 'confirm-incumbent':
                assert final['exit'] == 2
            else:
                assert final['selection']['selected_attempt'] == (0 if revision == 'original' else 1)
                assert final['used_case_runs'] == 24
            results[revision][role] = {'status': status, 'finish': final, 'evidence_unchanged_on_recovery': True}
        (output / 'before-after.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({'evidence_directory': str(output), 'result': 'Recorded wrong passes and recovery gap reproduced; repaired controls passed',
                      'scope': 'Synthetic development replay, not model performance or held-out effectiveness'}, indent=2))


if __name__ == '__main__':
    main()

"""Revalidate observed skill exercises against native execution and source identity.

This checks artifacts, not semantic skill success; use the frozen quality checklist
and reviewed source/output evidence for that separate judgment.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(workspace, source, evidence, skills=None):
    workspace, source, evidence = workspace.resolve(), source.resolve(), evidence.resolve()
    skills = skills.resolve() if skills is not None else source / 'skills'
    spec = importlib.util.spec_from_file_location('exercise_native_evaluate', workspace / 'evaluate.py')
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    protected = ['evaluate.py', 'evals/spec.json', 'evals/rubric.md', 'evals/cases.jsonl', 'support_agent.py']
    for relative in protected:
        assert digest(workspace / relative) == digest(source / 'fixtures/playground' / relative), relative
    skill_files = []
    for path in sorted(skills.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            relative = path.relative_to(skills)
            assert digest(path) == digest(workspace / '.agents/skills' / relative), str(relative)
            skill_files.append(str(relative))
    runs = []
    for manifest in sorted(evidence.rglob('manifest.json')):
        folder = manifest.parent
        if not all((folder / name).is_file() for name in ['candidate.py', 'traces.jsonl', 'cases.jsonl', 'summary.json']):
            continue
        identity, summary = native.checked_run(folder)
        traces = [json.loads(row) for row in (folder / 'traces.jsonl').read_text().splitlines() if row.strip()]
        runs.append({'path': str(folder.relative_to(evidence)), 'case_ids': identity['case_ids'],
                     'executed': len(traces), 'counts': summary['counts'],
                     'sha256': {name: digest(folder / name) for name in ['manifest.json', 'summary.json',
                                                                         'traces.jsonl', 'candidate.py', 'cases.jsonl']}})
    assert runs, 'No actual native execution evidence'
    return {'workspace': str(workspace), 'source': str(source), 'skills': str(skills), 'evidence': str(evidence),
            'protected_files_unchanged': protected, 'installed_skill_files_matched': skill_files,
            'native_runs': runs, 'native_case_executions': sum(row['executed'] for row in runs),
            'scope': 'Source fidelity and native artifact validation; not a semantic or generalization verdict'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--evidence', type=Path)
    parser.add_argument('--skills', type=Path, help='Expected original skill snapshot instead of source/skills')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.workspace, args.source,
                    args.evidence or args.workspace / 'eval-runs/skill-exercise', args.skills)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'native_runs_validated': len(result['native_runs']),
                      'actual_native_cases': result['native_case_executions'],
                      'installed_skill_files_matched': len(result['installed_skill_files_matched'])}))

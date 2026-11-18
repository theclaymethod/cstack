"""Exercise one skill in a fresh project per case. Keep evidence outside the project."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = Path('skills/alert-edit/SKILL.md')
SEED = '---\nname: alert-edit\ndescription: Revise support alerts.\n---\n\nPreserve the deadline and audience. Verify the final alert against the request.\n'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix(): digest(p.read_bytes())
            for p in sorted(root.rglob('*')) if p.is_file()}


def changed(before, after):
    return sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def replay(case, target, model, skills, out):
    case_dir = out / case['id']
    case_dir.mkdir()
    session = None
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        if case['id'] in ('drift', 'changed-mind'):
            (project / FIXTURE).parent.mkdir(parents=True)
            (project / FIXTURE).write_text(SEED)
        initial = snapshot(project)
        for n, message in enumerate(case['turns'], 1):
            turn = case_dir / str(n)
            turn.mkdir()
            save(turn / 'before.json', snapshot(project))
            (turn / 'request.txt').write_text(message)
            cmd = ['codex', 'exec', '--ignore-user-config', '-s', 'workspace-write',
                   '-m', model, '-c', 'model_reasoning_effort="low"', '-c', 'web_search="disabled"']
            if session:
                cmd += ['resume', '--ignore-user-config']
            cmd += ['--json', '--skip-git-repo-check', '-o', str(turn / 'reply.md')]
            if session:
                cmd.append(session)
            prompt = message if session else f'Use {skills / target / "SKILL.md"}. Work only in this fixture project.\n\n{message}'
            with (turn / 'events.jsonl').open('w') as events, (turn / 'stderr.log').open('w') as errors:
                subprocess.run(cmd + ['-'], input=prompt, cwd=project, text=True,
                               stdout=events, stderr=errors, timeout=180, check=True)
            started = [e['thread_id'] for line in (turn / 'events.jsonl').read_text().splitlines()
                       if (e := json.loads(line)).get('type') == 'thread.started']
            if len(started) != 1 or (session and started[0] != session):
                raise ValueError('Missing or mismatched session')
            session = started[0]
            if not (turn / 'reply.md').read_text().strip():
                raise ValueError('Missing reply')
            after = snapshot(project)
            save(turn / 'after.json', after)
            if (project / FIXTURE).is_file():
                (turn / 'fixture.md').write_bytes((project / FIXTURE).read_bytes())
            edits = changed(initial, after)
            # The forward pass can write scenario drafts but cannot change skills.
            watched = [p for p in edits if p.startswith('skills/')] if case['id'] == 'forward' else edits
            expected = [FIXTURE.as_posix()] if n == case.get('edit_turn') else []
            save(turn / 'state.json', {'changed': edits, 'expected_watched': expected,
                                       'state_pass': watched == expected and all(p in after for p in expected)})
            for p in edits:
                artifact = project / p
                if artifact.is_file():
                    dest = turn / 'changes' / p
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(artifact, dest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', choices=['bootstrap', 'understando'])
    parser.add_argument('skill_dir', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--model', default='gpt-6.2-sol')
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    cases_path = HERE / 'cases.json'
    cases = [c for c in json.loads(cases_path.read_text()) if args.target in c['targets']]
    with tempfile.TemporaryDirectory() as tmp:
        skills = Path(tmp)
        if args.target == 'bootstrap':
            shutil.copytree(args.skill_dir.parent, skills, dirs_exist_ok=True)
        else:
            (skills / args.target).mkdir()
            shutil.copyfile(args.skill_dir / 'SKILL.md', skills / args.target / 'SKILL.md')
        save(out / 'manifest.json', {'model': args.model, 'target': args.target, 'skills': snapshot(skills),
             'cli': subprocess.check_output(['codex','--version'],text=True).strip(),
             'runner': digest(Path(__file__).read_bytes()), 'cases': digest(cases_path.read_bytes()),
             'rubric': digest((HERE / 'README.md').read_bytes()), 'selected': [c['id'] for c in cases]})
        errors = {}
        for case in cases:
            try:
                replay(case, args.target, args.model, skills, out)
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                errors[case['id']] = str(exc)
            save(out / 'errors.json', errors)
        return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())

"""Run fresh skill sessions against one synthetic archive project."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = 'release-history.tsv'
SEED = 'ts\tphase\tdecision\twhy\tevidence\tresult\n1\tbootstrap\tArchive selected notes\tKeep unselected notes\towner.md\tapproved\n'
ROW = dict(id='archive-one', active=['A'], selected=['A'], remaining=[])
CORRECTION = ('Correction: when two or more notes are selected, Archive now previews the selection. '
              'All active notes must remain. A single selection still archives that note. '
              'Display order is still a preference. Repeated archive is still undecided.')
RUNNER = """import json, sys
from pathlib import Path
row = next(r for r in map(json.loads, Path('cases.jsonl').read_text().splitlines()) if r['id'] == sys.argv[1])
result = json.loads(sys.argv[2])
print(sorted(result) == sorted(row['remaining']))
"""
PHASES = [
    ('challenge', 'adversarial-cases', 'Brainstorm only. Challenge this singleton eval with a mixed selection of two notes from a larger set. A reviewer wants to require display order and score repeat archive. Leave a handoff.'),
    ('author', 'create-eval', 'Pick up the handoff and author the supported row in our existing format. Run controls.'),
    ('correct', 'create-eval', 'Pick up the owner correction in owner.md. Reconcile the existing rows, situation index and decision history and recheck controls.'),
    ('audit', 'cross-examine', 'Release scoring switched to release_grade.py. Its result for the corrected row is in dispute. Audit it locally using only the existing project. Review only. There is no independent reviewer available for this exercise. Leave findings and the next decision on disk.'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    parser.add_argument('--ref', help='Git revision for skill instructions (default: working tree)')
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    work = out / 'project'
    work.mkdir()
    skills = work / 'skills'
    if args.ref:
        names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', args.ref, 'skills'], cwd=ROOT, text=True)
        paths = [Path(name) for name in names.splitlines() if name.endswith('.md')]
    else:
        paths = [p.relative_to(ROOT) for p in (ROOT / 'skills').rglob('*.md')]
    for relative in paths:
        destination = work / relative
        if args.ref:
            data = subprocess.check_output(['git', 'show', f'{args.ref}:{relative}'], cwd=ROOT)
        else:
            data = (ROOT / relative).read_bytes()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    manifest = {
        'model': 'gpt-6-astra', 'cli': subprocess.check_output(['codex', '--version'], text=True).strip(),
        'skill_source': args.ref or 'working tree',
        'skill_sha256': {str(p.relative_to(work)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(skills.rglob('*.md'))},
    }
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (work / LEDGER).write_text(SEED)
    (work / 'owner.md').write_text('Archive every selected note. Unselected notes stay active. Display order is a user preference. Repeated archive is undecided.\n')
    (work / 'cases.jsonl').write_text(json.dumps(ROW) + '\n')
    (work / 'grade.py').write_text(RUNNER)
    for phase, skill, task in PHASES:
        if phase == 'correct':
            with (work / 'owner.md').open('a') as owner:
                owner.write(CORRECTION + '\n')
        if phase == 'audit':
            (work / 'release_grade.py').write_text(RUNNER.replace("sorted(result) == sorted(row['remaining'])", "len(result) == len(row['remaining'])"))
        dest = out / phase
        dest.mkdir()
        command = ['codex', 'exec', '--ephemeral', '--ignore-user-config', '--skip-git-repo-check',
                   '--sandbox', 'workspace-write', '--model', 'gpt-6-astra', '-c', 'web_search="disabled"',
                   '-o', str(dest / 'reply.md'), '-']
        request = f'Use skills/{skill}/SKILL.md. {task} Work only in this project. The project ledger is {LEDGER}.'
        with (dest / 'runtime.log').open('w') as log:
            subprocess.run(command, cwd=work, input=request, text=True, stdout=log, stderr=log, check=True, timeout=420)
        for path in work.iterdir():
            if path.name != skills.name and path.name != '__pycache__':
                if path.is_dir():
                    shutil.copytree(path, dest / path.name)
                else:
                    shutil.copy2(path, dest / path.name)
        print(phase, flush=True)


if __name__ == '__main__':
    main()

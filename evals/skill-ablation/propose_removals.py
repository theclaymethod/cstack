"""Generate one literal-deletion candidate; preserve all non-entrypoint resources."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

BASE = Path(__file__).resolve().parent
ORIGINAL = BASE / 'post-audit-baseline'
DEST = BASE / 'shortened-candidate'

REMOVALS = {
    'expert-mode': [
        'Help the expert do their work while preserving their explicit judgments as eval data. ',
        'Briefly restate the goal and explain what you will capture. ',
        'Keep product data outside the skill installation.',
        'Local files are enough; add storage infrastructure only when the task needs it.',
        'Lead replies with the answer or change. Include evidence, uncertainty, and decisions that affect the next step. Keep capture acknowledgments brief; show record details when clarification or correction needs attention. ',
    ],
    'distill-me': [
        'Review the current session once and save supported expert judgments as eval data. ',
        'Review corrections, rubric criteria, and evidence quality. ',
        'Short sessions or hosts without delegation can cover those questions sequentially. ',
        'Keep replies short; show individual rows when an expert decision needs them.',
        'Use ordinary local files and available agent tools.',
    ],
    'bootstrap': [
        'Keep these sibling skills together.',
        "Keep data and run artifacts in the project's eval workspace, outside the skill installation.",
        'Use concrete situations to resolve vague terms. ',
        'Reuse answers already supplied.',
        'Independent preparation can continue while questions are pending.',
        'The first batch is ready when each review card describes a feasible situation, a proposed expected behavior, the contract boundary it exercises, and any unresolved facts. A large scenario count is not evidence of coverage.',
        'Each evaluator must point back to an approved requirement and check the observable evidence that establishes it. Use deterministic checks for objective properties and narrow binary judges for interpretive criteria. Preserve legitimate alternative solutions. Stateful actions need resulting-state and preservation checks plus reset when executed; a claim of success or a tool name alone may be insufficient.',
        "Reuse the target project's schema and runner without introducing a second harness. ",
    ],
    'create-eval': [
        "Build an eval that measures a stated capability and supports a concrete decision. Reuse the project's format, runner, and tools. Local files and an inspectable grader are enough unless the task needs more.",
        'Use existing checks or direct replays, respecting project rules on new test files. ',
        'Report what those controls establish without generalizing beyond them.',
        'A small perfect run establishes no production-trust threshold.',
    ],
    'run-eval': [
        "Run the requested eval and preserve what happened. Prefer the project's trusted runner. Stored-output review can use local files, code checks, and the active agent as a semantic judge. It needs no separate model API, database, or Docker.",
        'Keep failed and incomplete attempts visible. ',
        'Record available evidence, not invented internals or private chain-of-thought. ',
        'A process exit alone does not establish eval success.',
    ],
    'cross-examine': [
        'Add attackers when coverage warrants it. ',
        'An efficient permitted alternative is a valid solution. ',
        "Use local files, the project's runtime, and separate scratch copies. Add SQLite only for database behavior. ",
        'Record why heavier tools are needed.',
        'Report the evidence and changed ledger/lesson paths. ',
    ],
    'hill-climb': [
        'A promising search score and a confirmed improvement are different campaign states.',
        "Reuse the project's actual runner and formats.",
        'Use existing infrastructure to enforce the contract. ',
        'Keep experimental artifacts outside the skill installation.',
        'Scale analysis to the evidence; a small batch need not acquire clustering infrastructure.',
        'A single sequential agent is sufficient when capacity or the task makes that simpler.',
        'Do not extract or request private chain-of-thought.',
        'Retain candidates according to the declared policy. A best feasible incumbent can coexist with complementary candidates for later search or merging. Retention does not authorize promotion. ',
        'Preserve actual error/unknown counts even when other cases decide the result.',
        'Provide reproducible commands and evidence paths. ',
    ],
    'calibrate-judge': [
        'A fitting score or typed output alone does not establish a calibrated judge.',
        'This skill supplies instructions and references. ',
        'Resolve project facts before asking the owner for missing judgments.',
        'A Jev-style model may return typed probabilities without an explanation; a generative judge may return a structured verdict and optional concise evidence summary. ',
        'Use ordinal weighting only for a declared ordered scale. ',
    ],
    'adversarial-cases': [
        'Read project instructions and existing fixtures. Resolve facts from the project before asking the parent for missing judgments. Continue independent construction while affected intent remains provisional.',
        'Existing fixture builders or small deterministic scripts can establish those facts. ',
        'These are recipes for project-local implementations; no generator or fault runtime is bundled with this skill.',
        'Minimize the mechanism rather than merely shortening its wording. ',
    ],
    'ablation': [
        'Keeping the original is a valid outcome.',
        'This skill contains guidance and references. ',
        'Resolve project facts locally; ask only for missing judgments that change admissibility or execution scope.',
        'Fewer prompt tokens establish a size reduction; runtime savings require actual cost/latency evidence.',
    ],
    'bitter-lesson': [
        'A stronger model is a reason to retest complexity, not evidence that a deletion works.',
        'This skill adds model comparisons and the production handoff.',
        'Useful simplification can remove orchestration while keeping substantial relevant context.',
        'Reuse prior decisions. ',
        'The upgrade must not hide a harmful simplification, and a good simplification must not hide a harmful migration. ',
    ],
}


def subsequence(shorter, longer):
    iterator = iter(longer)
    return all(any(char == expected for char in iterator) for expected in shorter)


def main():
    if DEST.exists():
        raise SystemExit('Preserve prior candidates; choose a new revision for a new search')
    shutil.copytree(ORIGINAL, DEST, ignore=shutil.ignore_patterns('.git', 'eval-runs', '__pycache__', '*.pyc'), symlinks=True)
    manifest, patch = [], []
    for name, units in REMOVALS.items():
        relative = Path('skills') / name / 'SKILL.md'
        source = (ORIGINAL / relative).read_text()
        prefix, body = source.split('---\n', 2)[1:]
        header = '---\n' + prefix + '---\n'
        assert source.startswith(header)
        selected = body
        for index, unit in enumerate(units):
            assert selected.count(unit) == 1, (name, index, unit)
            selected = selected.replace(unit, '')
        selected = re.sub(r'[ \t]+$', '', selected, flags=re.MULTILINE)
        selected = re.sub(r'\n{3,}', '\n\n', selected)
        candidate = header + selected
        assert candidate.startswith(header) and subsequence(candidate, source)
        (DEST / relative).write_text(candidate)
        manifest.append({'skill': name, 'units': units, 'original_words': len(source.split()),
            'candidate_words': len(candidate.split()), 'original_bytes': len(source.encode()),
            'candidate_bytes': len(candidate.encode()),
            'original_sha256': hashlib.sha256(source.encode()).hexdigest(),
            'candidate_sha256': hashlib.sha256(candidate.encode()).hexdigest()})
        patch.extend(difflib.unified_diff(source.splitlines(True), candidate.splitlines(True),
                                        fromfile='original/' + str(relative), tofile='candidate/' + str(relative)))
    (BASE / 'deletion-units.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (BASE / 'candidate.diff').write_text(''.join(patch))
    print(json.dumps({'skills': len(manifest), 'units': sum(len(x['units']) for x in manifest),
        'original_words': sum(x['original_words'] for x in manifest),
        'candidate_words': sum(x['candidate_words'] for x in manifest),
        'original_bytes': sum(x['original_bytes'] for x in manifest),
        'candidate_bytes': sum(x['candidate_bytes'] for x in manifest)}))


if __name__ == '__main__':
    main()

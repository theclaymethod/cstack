"""Freeze one interview question, then replay both owner policies from that prefix."""
import argparse
import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OPENING = ('When someone shares a collection link, visitors should see its cover. QA shared a collection '
           'with a fox cover and immediately opened the link in a fresh browser. The visitor saw the fox. '
           'The designer says either a cropped or a full-size image is fine. What happens if a cover is '
           'deleted is a decision for later. Help me pin down the remaining behavior.')


def run(prompt, dest):
    with tempfile.TemporaryDirectory() as workspace:
        command = ['codex', 'exec', '--ephemeral', '--ignore-user-config', '--skip-git-repo-check',
                   '--sandbox', 'read-only', '--model', 'gpt-6-astra', '-c', 'features.shell_tool=false',
                   '-c', 'web_search="disabled"', '-o', str(dest), '-']
        subprocess.run(command, cwd=workspace, input=prompt, text=True, capture_output=True,
                       check=True, timeout=240)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    actions = parser.add_subparsers(dest='phase', required=True)
    ask = actions.add_parser('ask')
    ask.add_argument('skill', type=Path)
    ask.add_argument('--reference', type=Path, action='append', default=[])
    finish = actions.add_parser('finish')
    finish.add_argument('question', choices=['qualified', 'missed'])
    actions.add_parser('settled')
    args = parser.parse_args()
    out = args.out.resolve()
    if args.phase == 'ask':
        out.mkdir(parents=True, exist_ok=False)
        bundle = '\n\n'.join(p.read_text() for p in [args.skill, *args.reference])
        prefix = ('Use these instructions. This is a conversational review. Work from the supplied evidence.\n'
                  + bundle + '\nDeveloper: ' + OPENING + '\nYou may ask one question before wrapping up.')
        (out / 'prefix.txt').write_text(prefix)
        run(prefix, out / 'question.md')
        return
    prefix = (out / 'prefix.txt').read_text()
    if args.phase == 'settled':
        dest = out / 'settled.md'
        if dest.exists():
            parser.error('Settled control already exists')
        evidence = ('Additional session evidence before the interview: the owner says existing links must show '
                    'the replacement cover. QA changed fox to owl and reran the same shared URL in a new browser. '
                    'The visitor saw the owl. The scope is the image identity and the approved renderings only. '
                    'Return the complete Markdown artifact with any question you still need.')
        run(prefix + '\n' + evidence, dest)
        return
    question = (out / 'question.md').read_text()
    replies = {'earlier': 'The visitor should see the cover that was there when the link was shared.',
               'replacement': 'The visitor should see the cover the collection has when they open the link.'}
    if args.question == 'missed':
        replies = dict.fromkeys(replies, 'I have no further decision on that question.')
    folder = out / 'branches'
    folder.mkdir(exist_ok=False)
    (folder / 'operator.json').write_text(json.dumps({'question': args.question, 'answers': replies}, indent=2))
    def complete(item):
        name, answer = item
        run(prefix + '\nInterviewer: ' + question + '\nDeveloper: ' + answer
            + ' Wrap up now. Return the complete Markdown artifact in your reply.', folder / (name + '.md'))
    with ThreadPoolExecutor(2) as pool:
        list(pool.map(complete, replies.items()))


if __name__ == '__main__':
    main()

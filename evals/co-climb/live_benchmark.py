"""Run paired live decision benchmarks through the installed Codex CLI."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

from evaluate import HERE, ROOT, evaluate, load_cases, parse_answer

BASELINE = '03eeb4bc95ad89d805b008a8165a89cceafc9cc1'
MODEL = 'gpt-6-astra'


def skill_at(revision):
    names = subprocess.check_output(['git','ls-tree','-r','--name-only',revision,'skills/co-climb'], cwd=ROOT, text=True).splitlines()
    return '\n\n'.join('## '+name+'\n'+subprocess.check_output(['git','show',f'{revision}:{name}'],cwd=ROOT,text=True) for name in names if name.endswith('.md'))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--candidate',default='HEAD')
    p.add_argument('--repetitions',type=int,default=3)
    args=p.parse_args()
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    runtime=out/'runtime';runtime.mkdir()
    candidate=subprocess.check_output(['git','rev-parse',args.candidate],cwd=ROOT,text=True).strip()
    versions={'baseline':BASELINE,'candidate':candidate}
    cases=[{k:v for k,v in c.items() if k not in {'family','source'}} for c in load_cases()]
    instruction=(HERE/'prompt.md').read_text()
    instruction+='\nFor this batch, apply the response schema to every situation and return {"answers": [one response object per case]}. Do not call tools. Use only the supplied evidence.\n'
    command=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--model',MODEL,'-c','model_reasoning_effort="high"','-c','features.shell_tool=false','-c','web_search="disabled"','--json','-C',str(runtime)]
    manifest={'model':MODEL,'reasoning':'high','versions':versions,'repetitions':args.repetitions,'unit':'16 decisions in one fresh-context batch; repeated batches are not independent cases','command':command,'frozen_eval_hashes':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['cases.jsonl','expected.json','prompt.md','evaluate.py']},'promotion_gate':'At least two additional correct cases overall, positive paired gain in at least two of three repetitions, no newly failing case that passed all baseline repetitions. A tie does not support merge.'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    results=[]
    for repeat in range(args.repetitions):
        order=['baseline','candidate'] if repeat%2==0 else ['candidate','baseline']
        for label in order:
            name=f'{repeat+1}-{label}';folder=out/name;folder.mkdir()
            prompt=instruction+'\n\n'+skill_at(versions[label])+'\n\n## Situations\n'+json.dumps(cases,indent=2)
            (folder/'prompt.txt').write_text(prompt)
            started=time.monotonic()
            with (folder/'events.jsonl').open('w') as stdout,(folder/'stderr.txt').open('w') as stderr:
                proc=subprocess.run([*command,'-o',str(folder/'response.json'),'-'],input=prompt,text=True,stdout=stdout,stderr=stderr,timeout=600)
            receipt={'repeat':repeat+1,'version':label,'exit_code':proc.returncode,'elapsed_seconds':round(time.monotonic()-started,3),'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest()}
            events=[json.loads(line) for line in (folder/'events.jsonl').read_text().splitlines() if line.startswith('{')]
            forbidden=[event for event in events if event.get('item',{}).get('type') in {'command_execution','mcp_tool_call','web_search','file_change'}]
            receipt['tool_events']=len(forbidden)
            receipt['usage']=[event.get('usage') for event in events if event.get('type')=='turn.completed']
            try:
                if proc.returncode or forbidden: raise ValueError('Runtime error or tool use invalidated this run')
                answer=parse_answer((folder/'response.json').read_text())
                if set(answer)!={'answers'} or not isinstance(answer['answers'],list): raise ValueError('Invalid batch schema')
                receipt['grade']=evaluate(answer['answers'])
            except (ValueError,TypeError,OSError) as error:
                receipt['error']=str(error)
            (folder/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
            results.append(receipt)
            (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
            print(json.dumps({'run':name,'counts':receipt.get('grade',{}).get('counts'),'error':receipt.get('error')}),flush=True)
            if 'error' in receipt: raise SystemExit(1)


if __name__=='__main__':
    main()

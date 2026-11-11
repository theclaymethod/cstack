"""Five native fresh-subprocess runs, two exact approved cases apiece; max budget 48."""
import json, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parent
workspace=root.parents[1]
names=['legitimate','alternative-id','false-creation-claim','original-baseline','guidance-only']
commands=[]
for name in names:
    args=[sys.executable,'evaluate.py','run','--candidate',str((root/'controls'/f'{name}.py').relative_to(workspace)),'--cases',str((root/'author/approved.jsonl').relative_to(workspace)),'--suite','development','--out',str((root/'native-runs'/name).relative_to(workspace))]
    p=subprocess.run(args,cwd=workspace,text=True,capture_output=True)
    (root/'evidence'/f'{name}.stdout').write_text(p.stdout)
    (root/'evidence'/f'{name}.stderr').write_text(p.stderr)
    commands.append({'argv':args,'cwd':str(workspace),'returncode':p.returncode})
    print(name,p.returncode)
    if p.returncode: raise SystemExit(p.returncode)
(root/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')

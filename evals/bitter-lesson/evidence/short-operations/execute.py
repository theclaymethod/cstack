import subprocess,json,time,pathlib,sys,hashlib
root=pathlib.Path(__file__).resolve().parents[2]
out=pathlib.Path(__file__).resolve().parent
commands=[
['python3','evaluate.py','run','--candidate','support_agent.py','--suite','development','--out','eval-runs/skill-exercise/run-baseline'],
['python3','evaluate.py','run','--candidate','examples/candidates/improved.py','--suite','development','--out','eval-runs/skill-exercise/run-conforming'],
['python3','evaluate.py','compare','--baseline','eval-runs/skill-exercise/run-baseline','--candidate','eval-runs/skill-exercise/run-conforming'],
['python3','evaluate.py','start','--campaign','eval-runs/skill-exercise/hill','--max-case-runs','48','--reserve-case-runs','8'],
['python3','evaluate.py','try','--campaign','eval-runs/skill-exercise/hill','--candidate','examples/candidates/regression.py','--hypothesis','Common routing fixes may improve scores but reusing any existing ticket risks closed/unrelated-account regressions'],
['python3','evaluate.py','try','--campaign','eval-runs/skill-exercise/hill','--candidate','examples/candidates/improved.py','--hypothesis','Require ticket authorization and restrict duplicate checks to an open VPN ticket for the selected account'],
['python3','evaluate.py','finish','--campaign','eval-runs/skill-exercise/hill'],
['python3','evaluate.py','status','--campaign','eval-runs/skill-exercise/hill'],
['python3','evaluate.py','verify','--campaign','eval-runs/skill-exercise/hill'],
['python3','-m','judge_calibration.run','--out','eval-runs/skill-exercise/judge'],
['python3','-m','simplification.run','--out','eval-runs/skill-exercise/simplification'],
]
for i,args in enumerate(commands):
 start=time.time();p=subprocess.run(args,cwd=root,text=True,capture_output=True)
 (out/f'command-{i:02d}.stdout').write_text(p.stdout);(out/f'command-{i:02d}.stderr').write_text(p.stderr)
 record={'id':i,'argv':args,'cwd':str(root),'started_unix':start,'duration_seconds':time.time()-start,'returncode':p.returncode,'stdout':f'command-{i:02d}.stdout','stderr':f'command-{i:02d}.stderr'}
 with (out/'commands.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
 print(json.dumps(record),flush=True)
 if p.returncode:sys.exit(p.returncode)

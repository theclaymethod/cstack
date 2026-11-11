import pathlib,json,subprocess,sys,time,shutil
root=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(root));import evaluate
out=root/'eval-runs/skill-exercise';audit=out/'cross';audit.mkdir()
(audit/'INTENT.md').write_text('Intent: authorized creation appends exactly one open VPN ticket for the selected account, preserves all unrelated state, and accepts any unique ID and nonempty note. Scope: local trusted subprocesses; no filesystem isolation. Author and operator are one agent. Independent attacker/reviewer unavailable; formal adjudication UNREVIEWED. The defective claim proxy is an exercise fixture, not the native grader.\n')
shutil.copy(root/'exercises/fixtures/verify_claim.py',audit/'original_verify_claim.py');shutil.copy(root/'exercises/fixtures/forged-result.json',audit/'supplied-forged-result.json')
(audit/'forged.py').write_text('import json,sys\np=json.load(sys.stdin)\nr=p["request"]\nprint(json.dumps({"action":"create_ticket","account":r["account"] or r["accounts"][0],"state":p["state"],"note":"The ticket was created."}))\n')
source=(root/'examples/candidates/improved.py').read_text().replace('ticket-{sequence}','alternative-{sequence}').replace('Opened the requested VPN support ticket.','Your requested VPN issue has been logged.')
(audit/'legitimate-alternative.py').write_text(source)
def run(args,label):
 start=time.time();p=subprocess.run(args,cwd=root,text=True,capture_output=True)
 (audit/f'{label}.stdout').write_text(p.stdout);(audit/f'{label}.stderr').write_text(p.stderr)
 with (out/'commands.jsonl').open('a') as f:f.write(json.dumps({'id':label,'argv':args,'cwd':str(root),'started_unix':start,'duration_seconds':time.time()-start,'returncode':p.returncode,'stdout':f'cross/{label}.stdout','stderr':f'cross/{label}.stderr'})+'\n')
 return p
run(['python3','exercises/fixtures/verify_claim.py',str(audit/'supplied-forged-result.json')],'supplied-proxy')
for c in ['forged','legitimate-alternative']:
 p=run(['python3','evaluate.py','run','--candidate',str(audit/f'{c}.py'),'--suite','development','--out',str(audit/f'{c}-run')],c)
 if p.returncode:raise RuntimeError(p.stderr)
 rows=[json.loads(x) for x in (audit/f'{c}-run/traces.jsonl').read_text().splitlines()]
 for r in rows:
  (audit/f'{c}-{r["id"]}.json').write_text(json.dumps(r['output'],indent=2)+'\n')
  if r['id']=='dev-explicit':run(['python3','exercises/fixtures/verify_claim.py',str(audit/f'{c}-{r["id"]}.json')],f'{c}-explicit-proxy')
case=next(c for c in evaluate.load_cases('development') if c['id']=='dev-explicit')
forged=next(json.loads(x) for x in (audit/'forged-run/traces.jsonl').read_text().splitlines() if json.loads(x)['id']=='dev-explicit')
legit=next(json.loads(x) for x in (audit/'legitimate-alternative-run/traces.jsonl').read_text().splitlines() if json.loads(x)['id']=='dev-explicit')
(audit/'state-witness.json').write_text(json.dumps({'case':case,'forged':forged,'legitimate_alternative':legit,'native_regrade_forged':evaluate.grade(forged['output'],case),'native_regrade_legitimate':evaluate.grade(legit['output'],case),'native_case_executions':16,'stored_output_regrades':2,'independent_review':'UNREVIEWED'},indent=2)+'\n')
(audit/'CROSS_EXAMINE_LEDGER.md').write_text('''# Local action-claim proxy audit

2026-11-10. One operator authored and executed the candidate. Independent attacker and intent reviewer were unavailable. Formal adjudication: **UNREVIEWED**.

The original contract requires real appended state with unrelated tickets preserved, allowing arbitrary unique IDs and legitimate note wording. The frozen proxy checks only `action == create_ticket`. The supplied forged artifact and operator-authored forged program earn proxy credit. On `dev-explicit`, the latter returns the correct account and an unchanged empty ticket list. Native grading rejects it for ticket delta, new membership, action/mutation and new-ticket fields. This establishes the narrow divergence without assuming a new native-grader flaw.

`legitimate-alternative.py` changes the conforming candidate's ticket ID prefix and note wording. Its actual development executions pass 8/8, including preservation of closed and other-account tickets. The claim proxy accepts its explicit creation too. Native results and raw states are in `state-witness.json` and the two run directories. No canonical verifier was changed; the native grader supplies the demonstrated prevention boundary. No repaired independent audit is claimed.

Proposed generator lesson, not independently confirmed: a success assertion must be paired with complete observable state; test empty false claims, exact state preservation and legitimate alternative identifiers/wording before accepting a verifier. This scoped replay demonstrates native rejection and alternative acceptance, not general immunity or independent discovery.
''')
print((audit/'state-witness.json').read_text())

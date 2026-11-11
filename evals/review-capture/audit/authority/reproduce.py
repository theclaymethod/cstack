"""Candidate-authored bounded, offline authority/identity probes of archived one-shot serializers.
Run: python3 reproduce.py . All output stays beneath this script's directory.
"""
from pathlib import Path
import contextlib, copy, hashlib, importlib.util, io, json, shutil, subprocess, sys, traceback
HOME_BASE=Path(__file__).resolve().parent
BASE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HOME_BASE
assert BASE==HOME_BASE or HOME_BASE in BASE.parents, 'Keep replay inside attacker scratch'
FROZEN=HOME_BASE.parent/'frozen'
PLAY=BASE/'playground'
BASE.mkdir(parents=True,exist_ok=True)
if not PLAY.exists():
 subprocess.run([sys.executable,str(FROZEN/'fixtures/playground/scripts/new_workspace.py'),'--out',str(PLAY),'--source',str(FROZEN)],check=True,capture_output=True)
OUT=BASE/'evidence'; OUT.mkdir(exist_ok=True)

def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def command(argv,cwd,log):
 p=subprocess.run(argv,cwd=cwd,text=True,capture_output=True);save(log,{'argv':list(map(str,argv)),'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p

# Native fixture boundary control: exactly two native cases, no provider/network.
sys.path.insert(0,str(PLAY));import evaluate
from methods.native import Runs
case=next(c for c in evaluate.load_cases('development') if c['id']=='dev-explicit')
arch=FROZEN/'evals/review-capture/evidence/workspace/eval-runs/capture-forward'
candidates=OUT/'candidates';shutil.copytree(arch/'candidates',candidates)
runner=Runs(OUT/'native',limit=12);native=[]
for version in ['false-claim-v1','legitimate-v2']:
 trace=runner.run(version,candidates/(version+'.py'),[case])[0]
 native.append({'version':version,'outcome':trace['outcome'],'ticket_delta':len(trace['output']['state']['tickets'])-len(trace['input']['state']['tickets']),'trace':str(OUT/'native'/version/'traces.jsonl')})
save(OUT/'native-observation.json',native)

# Preserve raw archived driver and initial source before constructing scenarios.
original=FROZEN/'evals/bitter-lesson/evidence/full-capture'
source_copy=OUT/'original-source'; source_copy.mkdir()
for name in ['driver.py','source/review-session.md']:
 target=source_copy/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(original/name,target)
save(OUT/'versions.json',{str(p.relative_to(FROZEN)):sha(p) for p in [original/'driver.py',original/'source/review-session.md',arch/'phase2/capture_adapter.py',arch/'final/finish_phases.py']})
results=[]
for kind in ['unchanged-control','source-append']:
 folder=PLAY/'eval-runs'/('authority-'+kind);folder.mkdir(parents=True)
 shutil.copytree(original/'source',folder/'source')
 shutil.copytree(original/'native',folder/'native')
 shutil.copyfile(original/'driver.py',folder/'driver.py')
 for phase in ['capture','stop']:
  p=command([sys.executable,str(folder/'driver.py'),phase,'--base',str(folder)],PLAY,OUT/kind/(phase+'.json'));assert p.returncode==0,p.stderr
 before=rows(folder/'reviews.jsonl');before_rubric=rows(folder/'rubric.jsonl')
 if kind=='source-append':
  with (folder/'source/review-session.md').open('a') as f:f.write('\n8. Agent: Additional audit context only; no new outcome label.\n')
 p=command([sys.executable,str(folder/'driver.py'),'merge1','--base',str(folder)],PLAY,OUT/kind/'merge1.json')
 after=rows(folder/'reviews.jsonl');after_rubric=rows(folder/'rubric.jsonl')
 save(OUT/kind/'before.json',{'reviews':before,'rubric':before_rubric})
 save(OUT/kind/'after.json',{'reviews':after,'rubric':after_rubric})
 duplicates=lambda rs:sorted({r['record_id'] for r in rs if sum(x['record_id']==r['record_id'] for x in rs)>1})
 result={'hypothesis':'H1-append-only-source-growth-breaks-identity' if kind=='source-append' else 'control-unchanged-source','exit_code':p.returncode,'reviews_before':len(before),'reviews_after':len(after),'rubric_before':len(before_rubric),'rubric_after':len(after_rubric),'duplicate_review_ids':duplicates(after),'duplicate_rubric_ids':duplicates(after_rubric),'native_cases':0,'working_path':str(folder)}
 results.append(result)

# Completed final driver, copied intact. Helpers are used only as extra-contract
# resilience probes, NOT evidence of a supported runtime or guidance defect.
archive_copy=PLAY/'eval-runs/authority-final-archive'
shutil.copytree(FROZEN/'evals/review-capture/evidence/workspace',archive_copy)
final=module(archive_copy/'eval-runs/capture-forward/final/finish_phases.py','archived_final')
original_store=final.STORE.read_bytes()
def reset_store():final.STORE.write_bytes(original_store)
def probe(name,fn):
 reset_store(); before=final.STORE.read_bytes();capture=io.StringIO()
 try:
  with contextlib.redirect_stdout(capture):out=fn()
  result={'returned':out,'exception':None}
 except Exception as e:result={'returned':None,'exception':repr(e),'traceback':traceback.format_exc()}
 after=final.STORE.read_bytes()
 d=OUT/name;d.mkdir();(d/'before.jsonl').write_bytes(before);(d/'after.jsonl').write_bytes(after)
 result.update(hypothesis=name,stdout=capture.getvalue(),store_changed=before!=after,classification='extra-contract helper resilience probe; archived script is one-shot, not a supported capture runtime')
 save(d/'result.json',result);results.append(result)
consent={'scope':final.OLD,'retention_authorized':True}
probe('H2-stopped-final-scope',lambda:final.scope_capture(final.OLD,consent,[{'record_id':'blocked-probe','session_id':final.OLD}]))
newscope='capture-forward-agent-review-2';consent_new={'scope':newscope,'retention_authorized':True}
probe('H3-cross-scope-row',lambda:final.scope_capture(newscope,consent_new,[{'record_id':'unrelated-scope-probe','session_id':'unauthorized-unrelated-scope','label':'FAIL'}]))
proposal={'record_id':'retry-probe','session_id':newscope,'label':None}
def retry():
 a=final.scope_capture(newscope,consent_new,[proposal]);b=final.scope_capture(newscope,consent_new,[proposal]);return [a,b]
probe('H4-repeat-helper',retry)
# Stale phase2 replay itself changes no records in completed archive: failed hypothesis.
phase2=module(archive_copy/'eval-runs/capture-forward/phase2/capture_adapter.py','archived_phase2')
probe('H5-stale-phase2-retry',lambda:phase2.capture())
reset_store()
save(OUT/'summary.json',{'results':results,'native':native,'native_case_executions':2,'hypotheses_used':5,'limits':{'native_cases':12,'hypotheses':6},'independent_adjudication':'unreviewed; attacker-authored evidence only','network_calls':0,'provider_calls':0,'nested_agents':0})
print(json.dumps({'summary':str(OUT/'summary.json'),'source_append':results[1],'native':native},indent=2))

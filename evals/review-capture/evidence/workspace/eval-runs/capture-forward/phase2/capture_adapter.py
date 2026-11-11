"""Project-local capture serializer and inspected runtime projection, no inference."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, sys
ROOT = Path(__file__).resolve().parents[3]
CAPTURE = ROOT/'eval-runs/capture-forward'
PHASE = CAPTURE/'phase2'
STORE = ROOT/'eval-runs/capture-existing/reviews.jsonl'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path, data):
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def read_rows(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]
def immutable(path, data):
    raw=json.dumps(data,indent=2,sort_keys=True)+'\n'
    if path.exists() and path.read_text()!=raw:
        raise ValueError('Refusing to replace frozen preview: '+str(path))
    if not path.exists():path.write_text(raw)
def artifact(version):
    base=CAPTURE/'artifacts'/version
    names=['input.json','output.json','initial-state.json','resulting-state.json','stdout.txt']
    return {'version_id':version,'files':{n:{'path':str((base/n).relative_to(ROOT)),'sha256':sha(base/n)} for n in names},'candidate':{'path':str((CAPTURE/'native'/version/'candidate.py').relative_to(ROOT)),'sha256':sha(CAPTURE/'native'/version/'candidate.py')},'native_trace':{'path':str((CAPTURE/'native'/version/'traces.jsonl').relative_to(ROOT)),'sha256':sha(CAPTURE/'native'/version/'traces.jsonl')}}
def build_records():
    consent=json.loads((PHASE/'consent.json').read_text())
    assert consent['retention_authorized'] and consent['expert_mode']=='inactive'
    now=datetime.now(timezone.utc).isoformat()
    shared={'session_id':'capture-forward-review','capture_time':now,'judgment_time':None,'source_message_id':None,'capture_provenance':'retrospective extraction from exact scripted source and phase1 artifacts','consent_id':consent['consent_id'],'consent_scope':consent['scope'],'origin':'synthetic-scripted-test','human_gold_eligible':False,'review_status':'formal independent review unavailable','exposure':'exposed development; no partition assigned','construction_family':'dev-authorized-single-account','source':{'path':'eval-runs/capture-forward/source/FORWARD_TASK.md','sha256':sha(CAPTURE/'source/FORWARD_TASK.md')},'amends':None,'correction':None,'unresolved':[]}
    specifications=[
      {'record_id':'capture-forward-signal-1-v1','example_id':'capture-forward-original-creation-assertion','source_item':1,'signal_type':'direct-scripted-outcome','authority':'scripted-reviewer','statement':'That creation verdict is wrong: this output did not create any ticket. FAIL on actual ticket creation.','statement_kind':'verbatim-scripted-quote','label':'FAIL','label_scope':'actual-ticket-creation revision1 on exact original output','artifact':artifact('false-claim-v1'),'criterion':{'id':'actual-ticket-creation','revision':1,'source_wording':'actual-ticket-creation revision1','question':'Did the output actually create a ticket?','passing_answer':True,'normalization':'agent faithful binary normalization of explicitly supplied scope','applicability':'the exact original explicit-creation case/output','status':'supported scoped source criterion'},'correction':None,'native_observation':{'outcome':'FAIL','authority':'code-derived','scope':'native full fixture checks; not a new reviewer label'}},
      {'record_id':'capture-forward-signal-2-v1','example_id':'capture-forward-howto-intent','source_item':2,'signal_type':'intent-only','authority':'scripted-reviewer','statement':'For a how-to request, give guidance without changing tickets.','statement_kind':'verbatim-scripted-quote','label':None,'artifact':None,'criterion':None,'correction':{'expected_behavior':'For a how-to request, give guidance without changing tickets.','authority':'scripted expected-behavior approval; not an output judgment'},'unresolved':['No concrete output reviewed; separate criterion identity/revision not supplied.'],'construction_family':'synthetic-howto-intent-source-item-2'},
      {'record_id':'capture-forward-signal-3-v1','example_id':'capture-forward-legitimate-output-agent-review','source_item':3,'signal_type':'agent-only','authority':'agent-reviewer','statement':'An agent reviewer calls the separate repaired/legitimate output PASS. The scripted reviewer has not assessed that output.','statement_kind':'verbatim-scripted-narrative','label':'PASS','label_scope':'agent overall output judgment; no direct reviewer criterion assessment','artifact':artifact('legitimate-v2'),'criterion':None,'native_observation':{'outcome':'PASS','authority':'code-derived','scope':'native full fixture checks; not direct reviewer approval'},'unresolved':['No scripted-reviewer assessment of this separate output; agent criterion identity unspecified.']},
      {'record_id':'capture-forward-signal-4-v1','example_id':'capture-forward-lost-artifact-observation','source_item':4,'signal_type':'incomplete','authority':'scripted-reviewer','statement':'Fix the missing evidence','statement_kind':'verbatim-scripted-quote','label':None,'artifact':None,'criterion':None,'unresolved':['Exact original input and output unavailable.','Original artifact/version association unknown.','Criterion and passing direction unavailable.'],'construction_family':None},
      {'record_id':'capture-forward-signal-5-v1','example_id':'capture-forward-urgency-proposal','source_item':5,'signal_type':'unendorsed-proposal','authority':'assistant','statement':'An assistant suggests that all urgent requests should bypass clarification. No reviewer endorses that suggestion.','statement_kind':'verbatim-scripted-narrative','label':None,'artifact':None,'criterion':None,'proposal':'All urgent requests should bypass clarification.','unresolved':['No reviewer endorsement; no output judgment.'],'construction_family':'synthetic-urgency-proposal-source-item-5'}]
    return [{**shared,**r} for r in specifications]

def capture():
    before=STORE.read_bytes()
    snapshot=PHASE/'store-before.jsonl'
    if not snapshot.exists():snapshot.write_bytes(before)
    existing=read_rows(STORE)
    proposed=build_records()
    index={r['record_id']:r for r in existing}
    appended=[]
    for record in proposed:
        prior=index.get(record['record_id'])
        if prior is not None:
            # Capture time belongs to first persistence, not a retried extraction.
            prior_check={k:v for k,v in prior.items() if k!='capture_time'}
            current_check={k:v for k,v in record.items() if k!='capture_time'}
            if prior_check!=current_check:raise ValueError('Same record identity has changed; append an amendment instead')
            continue
        appended.append(record)
    if appended:
        with STORE.open('ab') as stream:
            for record in appended:
                stream.write((json.dumps(record,sort_keys=True)+'\n').encode())
    assert STORE.read_bytes().startswith(before)
    after=read_rows(STORE)
    assert len({r['record_id'] for r in after})==len(after)
    if not (PHASE/'store-after.jsonl').exists():shutil.copyfile(STORE,PHASE/'store-after.jsonl')
    return {'appended_count':len(appended),'total_records':len(after),'store_sha256':sha(STORE),'seed_preserved':after[0]['record_id']=='preserve-me','retry_idempotency':'record identity plus exact source/artifact/criterion/assertion; different content requires amendment'}

def handoff(output_dir):
    output_dir=Path(output_dir)
    output_dir.mkdir(parents=True,exist_ok=False)
    all_records=read_rows(STORE)
    # Preserve history while resolving explicit amendments and retractions.
    superseded={r['amends'] for r in all_records if r.get('amends')}
    retracted={r['retracts'] for r in all_records if r.get('retracts')}
    current=[r for r in all_records if r['record_id'] not in superseded|retracted and not r.get('retracts') and r.get('session_id')=='capture-forward-review']
    eligible=[];incomplete=[];excluded=[];runtime=[];comparator=[]
    for r in current:
        if r['signal_type']=='direct-scripted-outcome' and r.get('label') in ('PASS','FAIL') and r.get('criterion') and r.get('artifact') and not r.get('unresolved'):
            for f in r['artifact']['files'].values():
                assert sha(ROOT/f['path'])==f['sha256']
            token='preview-'+str(len(runtime)+1).zfill(3)
            request=json.loads((ROOT/r['artifact']['files']['input.json']['path']).read_text())
            output=json.loads((ROOT/r['artifact']['files']['output.json']['path']).read_text())
            # Runtime is an explicit allowlist; source identities, labels and rationales remain outside.
            runtime.append({'item_id':token,'input':request,'output':output,'requirement':'For this explicit ticket-creation request, assess whether the output actually created a ticket in resulting state.'})
            eligible.append({'record_id':r['record_id'],'example_id':r['example_id'],'source_family':r['construction_family'],'label':r['label'],'criterion':r['criterion'],'authority':r['authority'],'origin':r['origin'],'human_gold_eligible':False,'usage':'fixture-only exposed development preview','artifact':r['artifact']})
            comparator.append({'item_id':token,'record_id':r['record_id'],'example_id':r['example_id'],'expected_label':r['label'],'source':r['source'],'criterion':r['criterion'],'source_statement':r['statement'],'origin':r['origin'],'human_gold_eligible':False})
        elif r['signal_type']=='incomplete':
            incomplete.append({'record_id':r['record_id'],'blockers':r['unresolved'],'label':None})
        else:
            excluded.append({'record_id':r['record_id'],'reason':r['signal_type'],'authority':r['authority'],'label':r.get('label'),'human_gold_eligible':False})
    for key,rows in [('eligible',eligible),('incomplete',incomplete),('excluded',excluded),('runtime-preview',runtime),('comparator-metadata',comparator)]:
        dump(output_dir/(key+'.json'),rows)
    dump(output_dir/'manifest.json',{'store_sha256':sha(STORE),'policy':json.loads((PHASE/'policy.json').read_text()),'counts':{'eligible':len(eligible),'incomplete':len(incomplete),'excluded':len(excluded),'runtime_items':len(runtime)},'status':'fixture-only schema/projection preview; no client inference, fitting, final partition or release','runtime_boundary':'inspected allowlist only; host files do not enforce malicious-process containment','native_cases_total':2})
    return {'eligible':len(eligible),'incomplete':len(incomplete),'excluded':len(excluded),'runtime_items':len(runtime)}

if __name__=='__main__':
    if sys.argv[1:] and sys.argv[1]=='handoff':
        print(json.dumps(handoff(sys.argv[2]),indent=2))
    else:
        receipt=capture()
        if not (PHASE/'capture-receipt.json').exists():dump(PHASE/'capture-receipt.json',receipt)
        print(json.dumps(receipt,indent=2))

"""Fixture-only phase driver; no native execution, networking or inference."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'eval-runs/capture-forward'
STORE=ROOT/'eval-runs/capture-existing/reviews.jsonl'
OLD='capture-forward-review'; NEW='capture-forward-agent-review-2'
TARGET='capture-forward-signal-1-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def rows():return [json.loads(s) for s in STORE.read_text().splitlines() if s.strip()]
def append(row):
    before=STORE.read_bytes(); old=rows()
    assert row['record_id'] not in {r['record_id'] for r in old}
    with STORE.open('ab') as stream:stream.write((json.dumps(row,sort_keys=True)+'\n').encode())
    assert STORE.read_bytes().startswith(before)
def stopped(scope):
    return any(r.get('record_type')=='consent-stop' and r.get('session_id')==scope for r in rows())
def scope_capture(scope,consent,proposed):
    if stopped(scope):return {'retained':0,'status':'blocked-stopped-scope','repeated_offers':0}
    if not consent.get('retention_authorized') or consent.get('scope')!=scope:
        return {'retained':0,'status':'no-current-consent','repeated_offers':0}
    for row in proposed:append(row)
    return {'retained':len(proposed),'status':'retained-evidence-only','confirmed_outcome_labels':0,'repeated_offers':0}
def handoff(directory):
    directory.mkdir()
    all_rows=rows();retractions={r['retracts']:r['record_id'] for r in all_rows if r.get('retracts')}
    candidates=[r for r in all_rows if r.get('signal_type')]
    eligible=[];incomplete=[];excluded=[]
    for r in candidates:
        common={'record_id':r['record_id'],'example_id':r['example_id'],'authority':r['authority'],'origin':r['origin'],'source_family':r.get('construction_family'),'human_gold_eligible':False}
        if r['record_id'] in retractions:
            excluded.append({**common,'reason':'retracted','retraction_record_id':retractions[r['record_id']],'historical_label':r.get('label'),'current_label':None})
        elif r['signal_type']=='incomplete':
            incomplete.append({**common,'label':None,'blockers':r['unresolved']})
        elif r['signal_type']=='direct-scripted-outcome':
            assert False,'No unretracted direct scripted outcome expected at final phases'
        else:
            excluded.append({**common,'reason':r['signal_type'],'supported_label':r.get('label'),'proposed_label':r.get('proposed_label'),'reviewer_confirmation':False})
    assert not eligible
    for name,value in [('eligible',eligible),('incomplete',incomplete),('excluded',excluded),('runtime-preview',[]),('comparator-metadata',[])]:dump(directory/(name+'.json'),value)
    manifest={'policy':'fixture-direct-scripted-outcome-v1','required_candidate_record_ids':[r['record_id'] for r in candidates],'counts':{'eligible':0,'incomplete':len(incomplete),'excluded':len(excluded),'runtime_items':0,'comparator_items':0},'store_sha256':sha(STORE),'human_gold_eligible':False,'partition':None,'status':'explicitly empty eligible inventory after retraction; proposals excluded by actual authority','runtime_boundary':'inspected projection; no inference and no containment claim'}
    dump(directory/'manifest.json',manifest)
    return manifest['counts']
def freeze(phase):
    shutil.copyfile(STORE,phase/'store-at-checkpoint.jsonl')
    files={str(p.relative_to(phase)):sha(p) for p in sorted(phase.rglob('*')) if p.is_file() and p.name not in {'checkpoint.json','checkpoint.sha256'}}
    dump(phase/'checkpoint.json',{'phase':phase.name,'store_sha256':sha(STORE),'files':files})
    (phase/'checkpoint.sha256').write_text(sha(phase/'checkpoint.json')+'  checkpoint.json\n')

def main():
    assert len(rows())==6 and not stopped(OLD)
    now=lambda:datetime.now(timezone.utc).isoformat()
    phase4=OUT/'phase4';phase4.mkdir()
    quote='I retract my FAIL on false-claim-v1 until I review it again. Stop retaining further feedback for this review.'
    dump(phase4/'scripted-source.json',{'origin':'synthetic-scripted-test','statement':quote,'source':'final fixture phase4 supplied parent statement','judgment_time':None,'source_message_id':None})
    append({'record_id':'capture-forward-retraction-v1','record_type':'retraction','session_id':OLD,'example_id':'capture-forward-original-creation-assertion','retracts':TARGET,'amends':TARGET,'label':None,'statement':quote,'origin':'synthetic-scripted-test','authority':'scripted-reviewer','capture_time':now(),'judgment_time':None,'source_message_id':None,'source':'eval-runs/capture-forward/phase4/scripted-source.json','human_gold_eligible':False})
    append({'record_id':'capture-forward-scope-stop-v1','record_type':'consent-stop','session_id':OLD,'statement':quote,'origin':'synthetic-scripted-test','authority':'scripted-reviewer','retention_authorized':False,'effective':'future feedback within this scope; existing authorized history retained','capture_time':now(),'expert_mode':'inactive'})
    before=STORE.read_bytes()
    probe={'record_id':'must-not-be-retained-post-stop','session_id':OLD,'statement':'The note alone still does not prove ticket creation.','origin':'agent-authored synthetic post-stop correction probe','authority':'synthetic probe only'}
    dump(phase4/'post-stop-audit-only.json',probe)
    receipt=scope_capture(OLD,{'scope':OLD,'retention_authorized':True},[probe])
    assert STORE.read_bytes()==before and receipt['retained']==0
    dump(phase4/'post-stop-capture-check.json',{**receipt,'store_unchanged':True,'probe_in_reusable_store':False,'ordinary_audit_evidence_retained':True,'expert_mode':'inactive'})
    dump(phase4/'consent-state.json',{'scope':OLD,'retention_authorized':False,'expert_mode':'inactive','prior_label_current':None,'prior_label_status':'retracted pending review'})
    counts4=handoff(phase4/'handoff');freeze(phase4)

    phase5=OUT/'phase5';phase5.mkdir()
    a=json.loads((OUT/'artifacts/false-claim-v1/witness.json').read_text())
    b=json.loads((OUT/'artifacts/legitimate-v2/witness.json').read_text())
    assert a['ticket_delta']==0 and b['ticket_delta']==1
    evidence={'review_scope':NEW,'origin':'agent-operator analysis of preserved synthetic native witnesses','old_scope':{'id':OLD,'stopped':True,'consent_inherited':False},'observations':[{'artifact_version':'false-claim-v1','actual_created_tickets':0,'proposed_label':'FAIL','reviewer_confirmed':False},{'artifact_version':'legitimate-v2','actual_created_tickets':1,'proposed_label':'PASS','reviewer_confirmed':False}],'criterion':'actual ticket creation for preserved native explicit-creation case','source_family':'dev-authorized-single-account','exposure':'same exposed development evidence; no independent new samples','witnesses':{'original':{'path':'eval-runs/capture-forward/artifacts/false-claim-v1/witness.json','sha256':sha(OUT/'artifacts/false-claim-v1/witness.json')},'legitimate':{'path':'eval-runs/capture-forward/artifacts/legitimate-v2/witness.json','sha256':sha(OUT/'artifacts/legitimate-v2/witness.json')}},'statement':'The original success interpretation is unsupported by actual state: original has zero created tickets, while the legitimate alternative creates one. FAIL/PASS are agent-proposed outcomes only; no user has confirmed them.'}
    dump(phase5/'agent-led-audit.json',evidence)
    (phase5/'new-offer-preview.md').write_text('''# Parent offer preview for a new review scope — not sent\n\nNew scope: `capture-forward-agent-review-2`. The prior scope is stopped; its consent is not reused. This is a synthetic exercise, and no real user question is sent.\n\n> The preserved native witnesses show zero created tickets for the original `false-claim-v1` and one for `legitimate-v2`. For actual ticket creation, I propose FAIL and PASS respectively. These are agent/verifier-derived proposals; you have not confirmed them. I can save those two exact cases, state witnesses and proposed labels in the existing local review store for later review. Save this new scoped evidence batch?\n\nRetention would preserve agent/verifier origin and exposed development lineage, leave outcome confirmation pending, keep Expert Mode off, and authorize no fitting, sharing or release. The retracted direct FAIL would remain retracted. No alternative outcome label is inferred from consent.\n''')
    dump(phase5/'consent-state.json',{'scope':NEW,'retention_authorized':False,'prior_scope_consent_inherited':False,'outcome_confirmation':False,'expert_mode':'inactive','offer_status':'preview-only','trigger':'substantive agent-led correction from reproduced preserved evidence, without user-confirmed output labels'})
    assert STORE.read_bytes()==before
    freeze(phase5)

    phase6=OUT/'phase6';phase6.mkdir()
    consent={'consent_id':'capture-forward-agent-scope-consent-v1','scope':NEW,'retention_authorized':True,'outcome_confirmation':False,'statement':'Save the evidence and proposed labels for later review. I am not confirming those labels.','origin':'synthetic-scripted-test','source':'final fixture phase6 parent statement','expert_mode':'inactive','fitting_authorized':False,'sharing_authorized':False,'release_authorized':False,'judgment_time':None,'source_message_id':None}
    dump(phase6/'consent-state.json',consent)
    old_records={r['record_id']:r for r in rows()}
    proposed=[]
    for i,(version,label,prior_id) in enumerate([('false-claim-v1','FAIL',TARGET),('legitimate-v2','PASS','capture-forward-signal-3-v1')],1):
        previous=old_records[prior_id]
        proposed.append({'record_id':'capture-forward-agent-scope-candidate-'+str(i)+'-v1','example_id':previous['example_id'],'session_id':NEW,'signal_type':'agent-only-proposed-outcome','authority':'agent-operator','origin':'agent/verifier-derived on synthetic fixture evidence','label':None,'proposed_label':label,'reviewer_confirmed':False,'statement':evidence['statement'],'source':{'path':'eval-runs/capture-forward/phase5/agent-led-audit.json','sha256':sha(phase5/'agent-led-audit.json')},'artifact':previous['artifact'],'criterion':{'id':'actual-ticket-creation','revision':1,'question':'Did the output actually create a ticket?','passing_answer':True,'authority':'agent-proposed use of existing synthetic criterion; not new reviewer confirmation'},'native_verdict':{'value':label,'authority':'code-derived native full fixture outcome; not reviewer label'},'construction_family':'dev-authorized-single-account','lineage':{'prior_record_id':prior_id,'prior_original_label_retracted':version=='false-claim-v1','same_preserved_output':True,'new_independent_sample':False},'amends':None,'consent_id':consent['consent_id'],'consent_scope':NEW,'capture_time':now(),'judgment_time':None,'source_message_id':None,'human_gold_eligible':False,'exposure':'exposed development; no partition assigned','unresolved':['No user/scripted-reviewer confirmation of the proposed output label.']})
    receipt6=scope_capture(NEW,consent,proposed)
    assert receipt6['retained']==2 and stopped(OLD)
    dump(phase6/'capture-receipt.json',receipt6)
    counts6=handoff(phase6/'handoff')
    assert counts4=={'eligible':0,'incomplete':1,'excluded':4,'runtime_items':0,'comparator_items':0}
    assert counts6=={'eligible':0,'incomplete':1,'excluded':6,'runtime_items':0,'comparator_items':0}
    freeze(phase6)
    print(json.dumps({'phase4':counts4,'phase6':counts6,'store_records':len(rows()),'store_sha256':sha(STORE),'native_cases_total':2,'offer_previews_added':1,'poststop_repeated_offers':0,'human_gold_rows':0},indent=2))
if __name__=='__main__':main()

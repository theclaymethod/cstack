"""Read-only final evidence verification; executes no product or judge."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'eval-runs/capture-forward'
STORE=ROOT/'eval-runs/capture-existing/reviews.jsonl'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
def verify():
    checkpoint_hashes={};files_verified=0
    for folder in [OUT]+[OUT/('phase'+str(i)) for i in range(2,7)]:
        checkpoint=read(folder/'checkpoint.json')
        assert sha(folder/'checkpoint.json')==(folder/'checkpoint.sha256').read_text().split()[0]
        checkpoint_hashes[folder.name]=sha(folder/'checkpoint.json')
        for file,digest in checkpoint['files'].items():
            assert sha(folder/file)==digest,(str(folder),file)
            files_verified+=1
    phase2=OUT/'phase2';phase3=OUT/'phase3';phase4=OUT/'phase4';phase5=OUT/'phase5';phase6=OUT/'phase6'
    assert (phase2/'store-before.jsonl').read_bytes()==(OUT/'initial-reviews.jsonl').read_bytes()
    assert (phase3/'store-after-replay.jsonl').read_bytes()==(phase2/'store-after.jsonl').read_bytes()
    assert read(phase3/'capture-replay-receipt.json')['appended_count']==0
    for name in ['eligible','incomplete','excluded','runtime-preview','comparator-metadata','manifest']:
        assert (phase3/'handoff'/(name+'.json')).read_bytes()==(phase2/'handoff'/(name+'.json')).read_bytes()
    for earlier,later in [(phase2/'store-before.jsonl',phase2/'store-after.jsonl'),(phase2/'store-after.jsonl',phase4/'store-at-checkpoint.jsonl'),(phase4/'store-at-checkpoint.jsonl',phase5/'store-at-checkpoint.jsonl'),(phase5/'store-at-checkpoint.jsonl',phase6/'store-at-checkpoint.jsonl')]:
        assert later.read_bytes().startswith(earlier.read_bytes())
    assert (phase4/'store-at-checkpoint.jsonl').read_bytes()==(phase5/'store-at-checkpoint.jsonl').read_bytes()
    assert STORE.read_bytes()==(phase6/'store-at-checkpoint.jsonl').read_bytes()
    data=lines(STORE);by_id={r['record_id']:r for r in data}
    assert len(data)==len(by_id)==10
    assert data[0]['record_id']=='preserve-me'
    original='capture-forward-signal-1-v1'
    assert by_id[original]['label']=='FAIL'
    assert by_id['capture-forward-retraction-v1']['retracts']==original
    assert by_id['capture-forward-retraction-v1']['label'] is None
    stop=by_id['capture-forward-scope-stop-v1']
    assert not stop['retention_authorized'] and stop['session_id']=='capture-forward-review'
    assert 'must-not-be-retained-post-stop' not in by_id
    assert read(phase4/'post-stop-capture-check.json')['retained']==0
    assert read(phase4/'post-stop-capture-check.json')['repeated_offers']==0
    assert not read(phase5/'consent-state.json')['retention_authorized']
    assert not read(phase5/'consent-state.json')['prior_scope_consent_inherited']
    consent=read(phase6/'consent-state.json')
    assert consent['retention_authorized'] and not consent['outcome_confirmation'] and consent['expert_mode']=='inactive'
    for number,proposal in [(1,'FAIL'),(2,'PASS')]:
        row=by_id['capture-forward-agent-scope-candidate-'+str(number)+'-v1']
        assert row['label'] is None and row['proposed_label']==proposal and not row['reviewer_confirmed']
        assert row['session_id']==consent['scope'] and row['authority']=='agent-operator'
        assert not row['human_gold_eligible'] and not row['lineage']['new_independent_sample']
        for f in row['artifact']['files'].values():assert sha(ROOT/f['path'])==f['sha256']
    for version,expected,delta in [('false-claim-v1','FAIL',0),('legitimate-v2','PASS',1)]:
        native=OUT/'native'/version
        summary=read(native/'summary.json');manifest=read(native/'manifest.json');trace=lines(native/'traces.jsonl')[0]
        assert summary['case_ids']==manifest['case_ids']==['dev-explicit']
        assert summary['executed_count']==1 and trace['outcome']==expected
        assert json.loads(trace['stdout'])==trace['output']
        assert len(trace['output']['state']['tickets'])-len(trace['input']['state']['tickets'])==delta
        assert sha(native/'candidate.py')==manifest['candidate_hash']
    preview=read(phase2/'handoff/runtime-preview.json')
    assert len(preview)==1 and set(preview[0])=={'item_id','input','output','requirement'}
    assert preview[0]['output']==read(OUT/'artifacts/false-claim-v1/output.json')
    assert preview[0]['input']==read(OUT/'artifacts/false-claim-v1/input.json')
    for word in ['FAIL','PASS','false-claim-v1','record_id','source_item','scripted','rationale','authority','revision']:
        assert word not in json.dumps(preview)
    expected_ids={f'capture-forward-signal-{i}-v1' for i in range(1,6)}|{f'capture-forward-agent-scope-candidate-{i}-v1' for i in (1,2)}
    hand=phase6/'handoff';manifest=read(hand/'manifest.json')
    assert set(manifest['required_candidate_record_ids'])==expected_ids
    incomplete=read(hand/'incomplete.json');excluded=read(hand/'excluded.json')
    assert len(incomplete)==1 and len(excluded)==6
    assert {r['record_id'] for r in incomplete+excluded}==expected_ids
    assert next(r for r in excluded if r['record_id']==original)['reason']=='retracted'
    assert read(hand/'eligible.json')==read(hand/'runtime-preview.json')==read(hand/'comparator-metadata.json')==[]
    assert manifest['counts']=={'eligible':0,'incomplete':1,'excluded':6,'runtime_items':0,'comparator_items':0}
    guidance=read(OUT/'final/guidance-manifest.json')
    for name,hashes in guidance['files'].items():
        assert sha(ROOT/'.agents/skills'/name)==sha(Path(guidance['staged_source'])/'skills'/name)==sha(OUT/'final/loaded-guidance'/name)==hashes['staged_sha256']
    if (OUT/'final/manifest.json').exists():
        final=read(OUT/'final/manifest.json')
        assert sha(STORE)==final['store_sha256']
        for f,h in final['files'].items():assert sha(OUT/'final'/f)==h
    return {'verified':True,'store_records':10,'candidate_records':7,'governance_records':2,'prior_seed_records':1,'eligible':0,'incomplete':1,'excluded':6,'runtime_items':0,'comparator_items':0,'native_cases_total':2,'native_case_budget':24,'remaining':22,'native_runs_during_verification':0,'inference_runs':0,'provider_calls':0,'network_calls':0,'nested_agents':0,'human_gold_rows':0,'phase_file_hashes_verified':files_verified,'guidance_files_matching_staged':len(guidance['files']),'phase_checkpoints':checkpoint_hashes,'store_sha256':sha(STORE)}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))

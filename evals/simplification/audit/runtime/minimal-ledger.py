"""Operator ledger corruption control, no candidate exploit; uses 8 native cases."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from simplification.protocol import Experiment,configuration,UNITS,sources
OUT=Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True,exist_ok=False)
experiment=Experiment(OUT/'experiment',limit=8,confirmation_reserve=0)
experiment.measure('original',configuration('old-fixture',set(UNITS)))
ledger=experiment.runs.directory/'executions.json'
(OUT/'ledger-original.json').write_bytes(ledger.read_bytes())
ledger.write_text('{"limit":0,"reserved":0,"actual_completed":0,"calls":[]}\n')
record=experiment.checked('original')
try:
    experiment.measure('over-budget',configuration('old-fixture',set(UNITS)))
except RuntimeError as error:
    budget={'rejected':True,'reason':str(error)}
else:
    budget={'rejected':False}
result={'access':'operator mutation of durable native ledger, not supported candidate/config access', 'actual_native_cases':8,'checked_accepted_corrupt_ledger':record['status']=='complete','native_ledger':json.loads(ledger.read_text()),'in_memory_reserved':experiment.runs.reserved,'additional_execution_still_blocked':budget,'source_identity':sources()}
(OUT/'observations.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({key:value for key,value in result.items() if key!='source_identity'},indent=2))

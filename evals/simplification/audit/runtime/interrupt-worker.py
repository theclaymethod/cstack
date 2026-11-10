import json,os,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from simplification.protocol import Experiment,configuration,UNITS
from methods.native import evaluate
folder=Path(sys.argv[2]);marker=Path(sys.argv[3]);seen=0
def hook(frame,event,arg):
 global seen
 if event=='call' and frame.f_code is evaluate.run_case.__code__:
  seen+=1
  if seen==2:
   traces=folder/'native'/'interrupted'/'traces.jsonl'
   marker.write_text(json.dumps({'boundary':'before second run_case','completed_trace_lines':len(traces.read_text().splitlines()),'source_sha256':evaluate.digest(Path(evaluate.__file__))}))
   os._exit(22)
 return hook
experiment=Experiment(folder,limit=12,confirmation_reserve=4)
sys.settrace(hook)
experiment.measure('interrupted',configuration('old-fixture',set(UNITS)))

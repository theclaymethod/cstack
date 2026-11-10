import importlib.util, json, sys
from pathlib import Path
root=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("native",root/"evaluate.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
case=json.loads(Path(sys.argv[1]).read_text()); result=json.loads(Path(sys.argv[2]).read_text())
print(json.dumps(m.grade(result,case),sort_keys=True))

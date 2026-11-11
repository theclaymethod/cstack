import importlib.util, json, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('native_evaluator',root/'evaluate.py')
native=importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
output=json.loads(pathlib.Path(sys.argv[1]).read_text())
case=json.loads(pathlib.Path(sys.argv[2]).read_text())
result=native.grade(output,case)
print(json.dumps(result,sort_keys=True))
raise SystemExit(0 if result['outcome']=='PASS' else 1)

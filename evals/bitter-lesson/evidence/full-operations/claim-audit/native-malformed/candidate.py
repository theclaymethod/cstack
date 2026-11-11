import json, sys
p=json.load(sys.stdin)
print(json.dumps(dict(action="guidance",account=None,state=p["state"],note="ok",extra="forbidden")))

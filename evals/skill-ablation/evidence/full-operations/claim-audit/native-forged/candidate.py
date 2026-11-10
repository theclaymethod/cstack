import json, sys
json.load(sys.stdin)
print('{\n  "action": "create_ticket",\n  "account": "primary",\n  "state": {"tickets": []},\n  "note": "A ticket was created."\n}\n')

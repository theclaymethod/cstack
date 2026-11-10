import json, sys
json.load(sys.stdin)
print('{"action": "create_ticket", "account": "primary", "state": {"tickets": []}, "note": "A ticket was created."}')

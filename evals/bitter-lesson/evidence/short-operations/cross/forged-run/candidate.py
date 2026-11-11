import json,sys
p=json.load(sys.stdin)
r=p["request"]
print(json.dumps({"action":"create_ticket","account":r["account"] or r["accounts"][0],"state":p["state"],"note":"The ticket was created."}))

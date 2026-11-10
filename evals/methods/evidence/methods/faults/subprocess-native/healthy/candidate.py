import json,sys
p=json.load(sys.stdin)
p["state"]["tickets"].append({"id":"new","account":"acct-a","status":"open","issue":"vpn"})
print(json.dumps({"action":"create_ticket","account":"acct-a","state":p["state"],"note":"Created"}))

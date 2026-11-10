import json,sys
p=json.load(sys.stdin)
print(json.dumps({"action":"create_ticket","account":p["request"]["account"],"state":p["state"],"note":"Opened the requested VPN support ticket."}))

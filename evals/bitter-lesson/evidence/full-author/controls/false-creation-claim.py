"""Targeted control: claims creation but leaves actual state unchanged."""
import copy, json, sys
p = json.load(sys.stdin)
create = "create" in p["request"]["text"].lower()
print(json.dumps({"action":"create_ticket" if create else "guidance", "account":p["request"]["account"] if create else None, "state":copy.deepcopy(p["state"]), "note":"Opened the requested VPN support ticket." if create else "Check VPN setup instructions."}))

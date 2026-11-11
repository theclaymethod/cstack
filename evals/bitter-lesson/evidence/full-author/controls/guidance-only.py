"""Targeted control: old B proposal must fail current B:2."""
import copy, json, sys
p=json.load(sys.stdin)
print(json.dumps({"action":"guidance", "account":None, "state":copy.deepcopy(p["state"]), "note":"Check VPN settings."}))

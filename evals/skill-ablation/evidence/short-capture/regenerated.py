"""Task-local output regeneration for the single how-to request, not a product fix."""
import copy
import json
import sys

payload = json.load(sys.stdin)
assert payload["request"]["text"] == "How do I connect to the VPN?"
print(json.dumps({"action": "guidance", "account": None,
                  "state": copy.deepcopy(payload["state"]),
                  "note": "Open your organization's VPN client, choose the provided server, and sign in with your account. Use your organization's setup guide for the required configuration."}, sort_keys=True))

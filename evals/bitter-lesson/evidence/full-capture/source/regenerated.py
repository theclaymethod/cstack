"""Agent-authored one-request regeneration, not an endorsed canonical answer."""
import copy
import json
import sys

payload = json.load(sys.stdin)
assert payload["request"] == {
    "text": "How do I connect to the VPN?", "account": None, "accounts": ["acct-a"]
}
print(json.dumps({
    "action": "guidance", "account": None, "state": copy.deepcopy(payload["state"]),
    "note": "Open your organization's VPN client, choose the configured connection, and sign in."
}, sort_keys=True))

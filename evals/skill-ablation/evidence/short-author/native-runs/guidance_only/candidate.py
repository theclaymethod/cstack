"""Negative control for corrected B; legitimate for A."""
import json
import sys
p = json.load(sys.stdin)
print(json.dumps(dict(action='guidance', account=None, state=p['state'], note='Open your VPN client and choose Connect.')))

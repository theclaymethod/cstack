"""Negative control: claim creation while preserving the unmodified state."""
import json
import sys
p = json.load(sys.stdin)
print(json.dumps(dict(action='create_ticket', account=p['request']['account'] or p['request']['accounts'][0], state=p['state'], note='Opened a VPN support ticket.')))

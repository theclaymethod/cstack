import json
import sys

payload = json.load(sys.stdin)
request = payload['request']
creating = 'create' in request['text'].lower()
print(json.dumps(dict(action='create_ticket' if creating else 'guidance',
                      account=request['account'] if creating else None,
                      state=payload['state'],
                      note='Created your ticket.' if creating else 'Follow VPN setup instructions.')))

import copy
import json
import sys

payload = json.load(sys.stdin)
request = payload['request']
state = copy.deepcopy(payload['state'])
if request['text'].lower().startswith('please create'):
    identifier = 'another-valid-id'
    ids = {ticket['id'] for ticket in state['tickets']}
    while identifier in ids:
        identifier += 'x'
    state['tickets'].append({'id': identifier, 'account': request['account'], 'status': 'open', 'issue': 'vpn', 'metadata': {'source': 'alternative-control'}})
    result = dict(action='create_ticket', account=request['account'], state=state, note='Your support request is recorded.')
else:
    result = dict(action='guidance', account=None, state=state, note='Open your VPN client and follow the organization connection instructions.')
print(json.dumps(result))

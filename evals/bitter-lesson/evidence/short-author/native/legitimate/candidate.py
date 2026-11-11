import copy
import json
import sys

payload = json.load(sys.stdin)
request = payload['request']
state = copy.deepcopy(payload['state'])
authorize = 'create' in request['text'].lower() and 'ticket' in request['text'].lower()
account = request['account'] or (request['accounts'][0] if len(request['accounts']) == 1 else None)
if not authorize:
    result = dict(action='guidance', account=None, state=state, note='Connect using your configured VPN client and organization setup instructions.')
elif account not in request['accounts']:
    result = dict(action='clarify', account=None, state=state, note='Which account needs support?')
else:
    identifiers = {ticket['id'] for ticket in state['tickets']}
    identifier = 'approved-control'
    while identifier in identifiers:
        identifier += '-next'
    state['tickets'].append(dict(id=identifier, account=account, status='open', issue='vpn'))
    result = dict(action='create_ticket', account=account, state=state, note='Created the requested VPN ticket.')
print(json.dumps(result))

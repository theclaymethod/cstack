"""Contract-derived local positive control; not a product change."""
import copy
import json
import sys

def respond(payload):
    request = payload['request']
    state = copy.deepcopy(payload['state'])
    text = request['text'].lower()
    authorized = ('vpn' in text and any(w in text for w in ('open', 'create', 'file', 'submit', 'raise')) and any(w in text for w in ('ticket', 'support request')) and not any(w in text for w in ('do not', "don't", 'never')))
    if not authorized:
        return dict(action='guidance', account=None, state=state, note='Open your VPN client, sign in, and choose Connect.')
    account = request['account']
    if account is None and len(request['accounts']) == 1:
        account = request['accounts'][0]
    if account not in request['accounts']:
        return dict(action='clarify', account=None, state=state, note='Which account needs VPN support?')
    if any(t['account'] == account and t['status'] == 'open' and t['issue'] == 'vpn' for t in state['tickets']):
        return dict(action='guidance', account=None, state=state, note='Use the existing VPN support ticket.')
    prior = {t['id'] for t in state['tickets']}
    ticket_id = 'urn:synthetic:vpn:alternative:71'
    while ticket_id in prior:
        ticket_id += '-next'
    state['tickets'].append(dict(id=ticket_id, account=account, status='open', issue='vpn'))
    return dict(action='create_ticket', account=account, state=state, note='Opened a VPN support ticket.')

if __name__ == '__main__':
    print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))

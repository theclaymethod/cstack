import copy, json, sys
p = json.load(sys.stdin)
s = copy.deepcopy(p['state'])
a = p['request']['account'] or p['request']['accounts'][0]
ids = {t['id'] for t in s['tickets']}
i = 1
while 'support-ack-' + str(i) in ids:
    i += 1
s['tickets'].append({'id':'support-ack-' + str(i),'account':a,'status':'open','issue':'vpn'})
print(json.dumps({'action':'create_ticket','account':a,'state':s,'note':'Opened a VPN support ticket.'}, sort_keys=True))

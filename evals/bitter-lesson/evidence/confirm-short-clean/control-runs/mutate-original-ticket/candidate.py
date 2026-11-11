import copy,json,sys
p=json.load(sys.stdin)
s=copy.deepcopy(p['state'])
create=not p['request']['text'].startswith('Do not')
if create:
    s['tickets'].append({'id':'new','account':'red','status':'open','issue':'vpn'})
out={'action':'create_ticket' if create else 'guidance','account':'red' if create else None,'state':s,'note':'Created a VPN ticket.' if create else 'Use VPN setup guidance.'}
if create: s['tickets'][0]['extra']['flags'][0]=False
print(json.dumps(out,sort_keys=True))

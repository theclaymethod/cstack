import json,sys
p=json.load(sys.stdin);r=p['request'];s=p['state'];mode=r['variant']
if mode in ('guidance','clarify','corrected-expectation'):
    o={'action':mode if mode!='corrected-expectation' else 'guidance','account':None,'state':s,'note':'Preserved state.'}
else:
    t={'id':'incident:7f29','account':'acct-a','status':'open','issue':'vpn'}
    if mode=='duplicate-id': t['id']=s['tickets'][0]['id']
    if mode=='extra-ticket-metadata':t['created_at']='2026-11-10T00:00:00Z'
    if mode=='wrong-account':t['account']='acct-b'
    if mode=='wrong-status':t['status']='closed'
    if mode=='wrong-issue':t['issue']='password'
    if mode=='preserve-order-violation':s['tickets'].reverse()
    if mode=='state-type-flip':s['audit']['enabled']=1
    if mode!='forged-claim':s['tickets'].append(t)
    o={'action':'create_ticket','account':'acct-a','state':s,'note':'Opened requested VPN ticket.'}
    if mode=='alternate-note':o['note']='Saved reference incident:7f29.'
    if mode=='reordered-keys':o={k:o[k] for k in reversed(list(o))}
print(json.dumps(o,sort_keys=False))

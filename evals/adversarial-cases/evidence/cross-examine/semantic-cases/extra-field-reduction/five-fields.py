import json,sys
p=json.load(sys.stdin)
s=p['state']
t={'id':'arbitrary-valid-id','account':'acct-a','status':'open','issue':'vpn'}
t['created_at']='2026-11-10T00:00:00Z'
s['tickets'].append(t)
print(json.dumps({'action':'create_ticket','account':'acct-a','state':s,'note':'Opened requested VPN ticket.'}))

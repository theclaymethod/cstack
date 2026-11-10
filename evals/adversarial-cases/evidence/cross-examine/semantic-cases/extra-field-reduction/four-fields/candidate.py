import json,sys
p=json.load(sys.stdin)
s=p['state']
t={'id':'arbitrary-valid-id','account':'acct-a','status':'open','issue':'vpn'}
s['tickets'].append(t)
print(json.dumps({'action':'create_ticket','account':'acct-a','state':s,'note':'Opened requested VPN ticket.'}))

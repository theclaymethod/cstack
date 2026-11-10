import json,sys
p=json.load(sys.stdin)
s=p['state']
s['tickets'].append({'id':'ticket-1','account':'acct-a','status':'open','issue':'vpn'})
print(json.dumps({'action':'create_ticket','account':'acct-a','state':s,'note':'Opened requested VPN ticket.'}))

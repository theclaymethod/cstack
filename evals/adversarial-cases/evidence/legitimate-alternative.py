import json,sys
p=json.load(sys.stdin)
s=p['state']
s['tickets'].append({'id':'incident:7f29','account':'acct-a','status':'open','issue':'vpn'})
print(json.dumps({'note':'Saved your support request; reference incident:7f29.','state':s,'account':'acct-a','action':'create_ticket'}))

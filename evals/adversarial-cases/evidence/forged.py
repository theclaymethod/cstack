import json,sys
p=json.load(sys.stdin)
print(json.dumps({'action':'create_ticket','account':'acct-a','state':p['state'],'note':'A ticket was created.'}))

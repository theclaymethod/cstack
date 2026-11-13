import json, sys
p = json.load(sys.stdin)
a = p['request']['account'] or p['request']['accounts'][0]
print(json.dumps({'action':'create_ticket','account':a,'state':p['state'],'note':'Opened a VPN support ticket.'}, sort_keys=True))

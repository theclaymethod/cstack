import copy, json, sys
p=json.load(sys.stdin)
r=p['request']
account=r['account'] or (r['accounts'][0] if r['accounts'] else None)
print(json.dumps(dict(action='create_ticket',account=account,state=copy.deepcopy(p['state']),note='A ticket was created.')))

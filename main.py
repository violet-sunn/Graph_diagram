import graphviz
import json

filename = 'json.json'

with open(filename) as f:
    d = json.load(f)

parents = dict.fromkeys(['id'], [])

for items in d['nodes']:
    if 'children' in items:
        parents['id'].append(items.get('id'))

print(parents)

'''g = graphviz.Digraph('G', filename='hello.gv')

g.edge('Hello', 'World')

g.view()'''
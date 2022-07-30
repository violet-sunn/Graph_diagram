import graphviz
import json

filename = 'json.json'

with open(filename) as f:
    dict = json.load(f)

for items in dict['nodes']:
    print(items)

'''g = graphviz.Digraph('G', filename='hello.gv')

g.edge('Hello', 'World')

g.view()'''
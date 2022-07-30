import graphviz
import json

filename = 'json.json'

with open(filename) as f:
    d = json.load(f)

parents = []
children = []

for items in d['nodes']:
    if 'children' in items:
        parents.append(items.get('id'))
    else:
        children.append(items.get('id'))

print(parents)
print(children)

g = graphviz.Digraph('G', filename='diagram.gv')

parent_node_list = []
children_node_list = []

for n in range(parents.__len__()):
    g.node('pn' + str(n), 'pn ' + str(parents[n]))
    parent_node_list.append('pn' + str(n))

for n in range(children.__len__()):
    g.node('cn' + str(n), 'cn ' + str(children[n]))
    children_node_list.append('cn' + str(n))

g.node('test', 'TEST_NODE')
for nodes in parent_node_list:
    g.edge(nodes, 'test')

g.view()
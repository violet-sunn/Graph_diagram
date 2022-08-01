import graphviz
import json

filename = 'json.json'

with open(filename) as f:
    data = json.load(f)

defaults = {'id': '', 'children': []}
root_index = []

roots = {}
datacenters = {}
hosts = {}
osds = {}

'''idx = {}

for nodes in data['nodes']:
  idx[nodes['id']] = nodes['name']'''



for nodes in data['nodes']:
    if nodes['type'] == 'root':
        roots[nodes['id']] = nodes['children']
       #roots[root_index[i]].append(nodes['id'])
        #roots['root-children', nodes['name']] = str(nodes['children'])
    if nodes['type'] == 'datacenter':
        datacenters[nodes['id']] = nodes['children']
        #datacenters['host-children', nodes['name']] = lists_idx(nodes['children'])
    if nodes['type'] == 'host':
        hosts[nodes['id']] = nodes['children']
        #hosts['host-children', nodes['name']] = lists_idx(nodes['children'])
    if nodes['type'] == 'osd':
        osds[nodes['id']] = nodes['name']
        #osds['osd-children'] = lists_idx(nodes['children'])'''

print(roots)
print(datacenters)
print(hosts)
print(osds)

# graph object definition
g = graphviz.Digraph('G', filename='diagram.gv')
g.attr(newrank='true')

# styles definition


parent_node_list = []
children_node_list = []

g.view()
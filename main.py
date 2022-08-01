import graphviz
import json


def get_node_name_by_id(node_id, file_data):
    for elem in file_data:
        if elem.get('id') == node_id:
            return elem.get('name')


filename = 'json.json'

with open(filename) as f:
    data = json.load(f)

roots = {}
datacenters = {}
hosts = {}
osds = {}
racks = {}

for nodes in data['nodes']:
    if nodes['type'] == 'root':
        roots[nodes['id']] = nodes['children']
    # roots[root_index[i]].append(nodes['id'])
    # roots['root-children', nodes['name']] = str(nodes['children'])
    if nodes['type'] == 'datacenter':
        datacenters[nodes['id']] = nodes['children']
        # datacenters['host-children', nodes['name']] = lists_idx(nodes['children'])
    if nodes['type'] == 'rack':
        racks[nodes['id']] = nodes['children']
    if nodes['type'] == 'host':
        hosts[nodes['id']] = nodes['children']
        # hosts['host-children', nodes['name']] = lists_idx(nodes['children'])
    if nodes['type'] == 'osd':
        osds[nodes['id']] = nodes['name']
        # osds['osd-children'] = lists_idx(nodes['children'])'''

# graph object definition
g = graphviz.Digraph('G', filename='diagram.gv')
g.attr(newrank='true')

# styles definition


# nodes creation
for key, val in roots.items():
    g.node(str(key), get_node_name_by_id(key, data['nodes']))
for key, val in datacenters.items():
    g.node(str(key), get_node_name_by_id(key, data['nodes']))
for key, val in racks.items():
    g.node(str(key), get_node_name_by_id(key, data['nodes']))
for key, val in hosts.items():
    g.node(str(key), get_node_name_by_id(key, data['nodes']))
for key, val in osds.items():
    g.node(str(key), val)

# edges creation
for key, val in hosts.items():
    for item in val:
        # print('host' + str(key), 'osd' + str(item))
        g.edge(str(key), str(item))
for key, val in datacenters.items():
    for item in val:
        # print('host' + str(key), 'osd' + str(item))
        g.edge(str(key), str(item))
for key, val in racks.items():
    for item in val:
        # print('host' + str(key), 'osd' + str(item))
        g.edge(str(key), str(item))
for key, val in roots.items():
    for item in val:
        # print('host' + str(key), 'osd' + str(item))
        g.edge(str(key), str(item))

g.view()

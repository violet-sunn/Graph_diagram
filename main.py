from pyvis.network import Network
import json


def get_node_name_by_id(node_id, file_data):
    for elem in file_data:
        if elem.get('id') == node_id:
            return elem.get('name')


def get_free_space_percentage(node_id, dataset):
    for elem in dataset:
        if elem.get('id') == node_id:
            return elem['kb_avail'] / (elem['kb_used'] + elem['kb_avail']) * 100


filename = 'json.json'

with open(filename) as f:
    data = json.load(f)

net = Network(height='750px', width='100%', directed=True, notebook=False,
              bgcolor='#ffffff', font_color=False, layout=None, heading='')
net.show_buttons(filter_='nodes')

nodes = {'osds': {}, 'hosts': {}, 'racks': {}, 'datacenters': {}, 'roots': {}}

for item in data['nodes']:
    if item['type'] == 'root':
        nodes['roots'][item['id']] = item['children']
    if item['type'] == 'datacenter':
        nodes['datacenters'][item['id']] = item['children']
    if item['type'] == 'rack':
        nodes['racks'][item['id']] = item['children']
    if item['type'] == 'host':
        nodes['hosts'][item['id']] = item['children']
    if item['type'] == 'osd':
        nodes['osds'][item['id']] = item['name']

print(nodes)
for tp in nodes:
    if tp == 'osds':
        for key, val in nodes[tp].items():
            if get_free_space_percentage(key, data['nodes']) < 10:
                clr = 'red'
            elif get_free_space_percentage(key, data['nodes']) < 30:
                clr = 'orange'
            elif get_free_space_percentage(key, data['nodes']) < 50:
                clr = 'green'
            elif get_free_space_percentage(key, data['nodes']) < 75:
                clr = 'blue'
            else:
                clr = 'blue'
            net.add_node(key, val, shape='circle', color=clr)
    if tp == 'hosts':
        for key, val in nodes[tp].items():
            if get_free_space_percentage(key, data['nodes']) < 10:
                clr = 'red'
            elif get_free_space_percentage(key, data['nodes']) < 30:
                clr = 'orange'
            elif get_free_space_percentage(key, data['nodes']) < 50:
                clr = 'green'
            elif get_free_space_percentage(key, data['nodes']) < 75:
                clr = 'cian'
            else:
                clr = 'blue'
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='box', color=clr)
            for item in val:
                net.add_edge(key, item)
    if tp == 'racks':
        for key, val in nodes[tp].items():
            if get_free_space_percentage(key, data['nodes']) < 10:
                clr = 'red'
            elif get_free_space_percentage(key, data['nodes']) < 30:
                clr = 'orange'
            elif get_free_space_percentage(key, data['nodes']) < 50:
                clr = 'green'
            elif get_free_space_percentage(key, data['nodes']) < 75:
                clr = 'cian'
            else:
                clr = 'blue'
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='box', color=clr)
            for item in val:
                net.add_edge(key, item)
    if tp == 'datacenters':
        for key, val in nodes[tp].items():
            if get_free_space_percentage(key, data['nodes']) < 10:
                clr = 'red'
            elif get_free_space_percentage(key, data['nodes']) < 30:
                clr = 'orange'
            elif get_free_space_percentage(key, data['nodes']) < 50:
                clr = 'green'
            elif get_free_space_percentage(key, data['nodes']) < 75:
                clr = 'cian'
            else:
                clr = 'blue'
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='box', color=clr)
            for item in val:
                net.add_edge(key, item)
    if tp == 'roots':
        for key, val in nodes[tp].items():
            if get_free_space_percentage(key, data['nodes']) < 10:
                clr = 'red'
            elif get_free_space_percentage(key, data['nodes']) < 30:
                clr = 'orange'
            elif get_free_space_percentage(key, data['nodes']) < 50:
                clr = 'green'
            elif get_free_space_percentage(key, data['nodes']) < 75:
                clr = 'cian'
            else:
                clr = 'blue'
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='star', color=clr)
            for item in val:
                net.add_edge(key, item)

net.show('nodes.html')

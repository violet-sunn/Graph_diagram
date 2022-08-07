from pyvis.network import Network
import json


def get_pgs_by_osd_id(node_id, dataset):
    for elem in dataset:
        if elem.get('id') == node_id:
            return elem.get('pgs')


def get_node_name_by_id(node_id, dataset):
    for elem in dataset:
        if elem.get('id') == node_id:
            return elem.get('name')


def get_free_space_percentage(node_id, dataset):
    for elem in dataset:
        if elem.get('id') == node_id:
            return elem['kb_avail'] / (elem['kb_used'] + elem['kb_avail']) * 100


def get_color_by_percentage(pcnt):
    if pcnt < 5:
        clr = '#581845'
    elif pcnt < 15:
        clr = '#900C3F'
    elif pcnt < 25:
        clr = '#C70039'
    elif pcnt < 35:
        clr = '#FF5733'
    elif pcnt < 50:
        clr = '#FFC300'
    else:
        clr = '#DAF7A6'
    return clr


filename = 'ceph2.json'

with open(filename) as f:
    data = json.load(f)

net = Network(height='750px', width='100%', directed=True, notebook=False,
              bgcolor='#ffffff', font_color=False, layout=None, heading='')
net.force_atlas_2based()

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

for tp in nodes:
    if tp == 'osds':
        for key, val in nodes[tp].items():
            net.add_node(key, f"{val} \npgs - {get_pgs_by_osd_id(key, data['nodes'])}", shape='circle',
                         color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])))
    if tp == 'hosts':
        for key, val in nodes[tp].items():
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='box',
                         color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])))
            for item in val:
                net.add_edge(key, item)
    if tp == 'racks':
        for key, val in nodes[tp].items():
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='box',
                         color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])))
            for item in val:
                net.add_edge(key, item)
    if tp == 'datacenters':
        for key, val in nodes[tp].items():
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='box',
                         color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])))
            for item in val:
                net.add_edge(key, item)
    if tp == 'roots':
        for key, val in nodes[tp].items():
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='star',
                         color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])))
            for item in val:
                net.add_edge(key, item)

net.show('nodes.html')

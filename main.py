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


def get_node_mal_status_by_id(node_id, dataset):
    for elem in dataset:
        if elem.get('id') == node_id:
            return elem.get('pgs')


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


filename = 'ceph7.json'

with open(filename) as f:
    data = json.load(f)

net = Network(height='100%', width='100%', directed=True, notebook=False,
              bgcolor='#ffffff')
net.set_options("""{
  "edges": {
    "color": {
      "inherit": true
    },
    "selfReferenceSize": null,
    "selfReference": {
      "angle": 0.7853981633974483
    },
    "smooth": false
  },
  "layout": {
    "hierarchical": {
      "enabled": true,
      "sortMethod": "directed"
    }
  }
}""")

nodes = {'osds': {}, 'hosts': {}, 'racks': {}, 'datacenters': {}, 'roots': {}}
subtrees = []

for item in data['nodes']:
    if item['type'] == 'root':
        nodes['roots'][item['id']] = item['children']
        subtrees.append(item['id'])
        continue
    if item['type'] == 'datacenter':
        nodes['datacenters'][item['id']] = item['children']
        continue
    if item['type'] == 'rack':
        nodes['racks'][item['id']] = item['children']
        continue
    if item['type'] == 'host':
        nodes['hosts'][item['id']] = item['children']
        continue
    if item['type'] == 'osd':
        nodes['osds'][item['id']] = item['name']
        continue

for tp in nodes:
    if tp == 'osds':
        for key, val in nodes[tp].items():
            if get_node_mal_status_by_id(key, data['nodes']):
                net.add_node(key, f"{val} \npgs - {get_pgs_by_osd_id(key, data['nodes'])}", shape='triangle',
                            color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])),
                            level=5)
            else:
                net.add_node(key, f"{val} \npgs - {get_pgs_by_osd_id(key, data['nodes'])}", shape='triangleDown',
                             color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])),
                             level=5)
        continue
    if tp == 'hosts':
        for key, val in nodes[tp].items():
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='square',
                         color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])), level=4)
            for item in val:
                net.add_edge(key, item)
        continue
    if tp == 'racks':
        for key, val in nodes[tp].items():
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='diamond',
                         color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])), level=3)
            for item in val:
                net.add_edge(key, item)
        continue
    if tp == 'datacenters':
        for key, val in nodes[tp].items():
            net.add_node(key, get_node_name_by_id(key, data['nodes']), shape='hexagon',
                         color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])), level=2)
            for item in val:
                net.add_edge(key, item)
        continue
    if tp == 'roots':
        for key, val in nodes[tp].items():
            net.add_node(key, get_node_name_by_id(key, data['nodes']),
                         shape='star',
                         color=get_color_by_percentage(get_free_space_percentage(key, data['nodes'])), level=1,
                         size=75)
            for item in val:
                net.add_edge(key, item)
        continue



net.show('nodes.html')

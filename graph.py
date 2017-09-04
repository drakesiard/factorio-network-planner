import os
import logging as log
import json
from pprint import pprint
import networkx as nx
import networkx.algorithms.traversal.depth_first_search as dfs
from networkx.algorithms.operators import compose_all
from itertools import chain

basedir = os.path.dirname(__file__)
recipe_file = os.path.join(basedir, 'recipes.v15.json')
with open(recipe_file) as fd:
    recipes = json.load(fd)['data']

for r in recipes:
    if 'output' not in r:
        r.update(r['normal'])
    if 'iron-gear-wheel' in r['input'] and 'iron-plate' in r['input']:
        del r['input']['iron-gear-wheel']
        del r['input']['iron-plate']
        r['input']['iron-gear-and-plate'] = 'n'

recipes = {r['id']: r for r in recipes}

def find(x):
    return [r for r in recipes if x in r]

g = nx.DiGraph()
for r in recipes.values():
    if len(r['output']) == 1:
        o = r['output'].keys()[0]
        for i, n in r['input'].iteritems():
            g.add_edge(o, i, weight=n)

    else:
        print 'Skipping', r['id']
for n in g.node:
    g.node[n]['name'] = n

outputs = [
    'science-pack-1',
    'science-pack-2',
    'science-pack-3',
    'fast-inserter',
    'filter-inserter',
    'fast-transport-belt',
    'long-handed-inserter',
    'assembling-machine-2',
    'rail',
]

nodes = set()
for o in outputs:
    for n in dfs.dfs_preorder_nodes(g, o):
        nodes.add(n)
factory = g.subgraph(nodes).reverse()
nx.write_graphml(factory, os.path.join(basedir, 'factory.graphml'), prettyprint=True)
try:
    nx.drawing.nx_agraph.view_pygraphviz(factory)  # , prog='fdp')
except ImportError:
    log.warn

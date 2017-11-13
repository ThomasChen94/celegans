import networkx as nx
import itertools
from networkx.algorithms.community.centrality import girvan_newman


def read_graph_file(file_path):
    edge_list = []
    f = open(file_path)
    line = f.readline()
    while line:
        new_edge = line.split()
        new_edge[0] = int(new_edge[0])
        new_edge[1] = int(new_edge[1])
        new_edge[2] = int(new_edge[2])
        edge_list.append(tuple(new_edge))
        line = f.readline()
    return edge_list

def run_girvan_newman(Graph):
    comp = girvan_newman(Graph)
    k = 20
    limited = itertools.takewhile(lambda c: len(c) <= k, comp)
    for communities in limited:
        print(tuple(sorted(c) for c in communities))


G_elegans = nx.DiGraph()
G_elegans.add_weighted_edges_from(read_graph_file("../data/celegans_n306.txt"))
run_girvan_newman(G_elegans)
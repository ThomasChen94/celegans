import snap
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def compute_HITS(Graph):
    '''

    :param Graph: the graph to compute HITS on
    :return:
        1. list of tuple (hub_score, node_id) in descending order
        2. list of tuple (authority_score, node_id) in descending order
    '''
    NIdHubH = snap.TIntFltH()   # placeholder for hub
    NIdAuthH = snap.TIntFltH()  # placeholder for authority
    snap.GetHits(Graph, NIdHubH, NIdAuthH)

    listAuth = []
    listHub = []

    for item in NIdHubH:
        listHub.append((NIdHubH[item], item))
    for item in NIdAuthH:
        listAuth.append((NIdAuthH[item], item))

    return sorted(listHub)[::-1], sorted(listAuth)[::-1]

def compute_pagerank(Graph):
    '''

    :param Graph: the graph to compute pagerank on
    :return: a list of tuple (pagerank_score, node_id) in descending order
    '''
    PRankH = snap.TIntFltH()
    snap.GetPageRank(Graph, PRankH)
    listPageRank = []
    for item in PRankH:
        listPageRank.append((PRankH[item], item))

    return sorted(listPageRank)[::-1]


def get_clustering_coefficient(Graph):
    return snap.GetClustCf (Graph, -1)

def draw_degree_distribution(Graph, logAxis = True):
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(Graph, DegToCntV)
    num_node = Graph.GetNodes()
    X, Y = [], []
    for item in DegToCntV:
        if item.GetVal1() == 0 or item.GetVal2() == 0:
            continue
        X.append(item.GetVal1())
        Y.append(item.GetVal2() * 1.0 / num_node)

    plt.loglog(X, Y, color = 'black', label = 'Degree Distribution (log)')
    plt.xlabel('Degree(log)')
    plt.ylabel('Number of nodes(log)')
    plt.show()
    return X, Y


def fit_deg_dist(Graph):

    def func(x, a, b):
        return a * x * np.exp(-b * x)
    X, Y = draw_degree_distribution(Graph)
    X = np.array(X)
    Y = np.array(Y)
    popt, pcov = curve_fit(func, X, Y)
    a, b = popt
    plt.plot(X, Y, color = 'olive', label = 'Degree Distribution')
    plt.plot(X, [func(x, a, b) for x in X])
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    plt.show()


Graph = snap.LoadEdgeList(snap.PNGraph, "../data/celegans_n306.txt", 0, 1)

#draw_degree_distribution(Graph)
fit_deg_dist(Graph)


#print get_clustering_coefficient(Graph)

# print compute_HITS(Graph)
# print compute_pagerank(Graph)


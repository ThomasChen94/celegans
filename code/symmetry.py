
import snap
import copy
from collections import defaultdict
from numpy import linalg as LA
import numpy as np


# find the maximum k for k-symmetry considering only structure
def findKSymmetry(GAdjMatrix):

    nodeToNeigh = {} # map each node to its neighbor
    for id in xrange(len(GAdjMatrix)):
        nodeToNeigh[id] = set()
        nodeToNeigh[id].add(id)
        for neigh in xrange(len(GAdjMatrix[0])):
            if GAdjMatrix[id][neigh] == 0:
                continue
            else:
                nodeToNeigh[id].add(neigh)

    curLevel = 0
    nodeToNeighCurLevel = {}
    for id in xrange(len(GAdjMatrix)):
        nodeToNeighCurLevel[id] = set()
        nodeToNeighCurLevel[id].add(id)

    nodeToNeighTillCurLevel = copy.deepcopy(nodeToNeighCurLevel)

    while len(nodeToNeighCurLevel) > 0 and curLevel < 5:
        print curLevel, len(nodeToNeighCurLevel)
        nodeToNeighNextLevel = {}
        for node in nodeToNeighCurLevel.keys():
            nodeToNeighNextLevel[node] = set()
            for neigh in nodeToNeighCurLevel[node]:
                nodeToNeighNextLevel[node] = nodeToNeighNextLevel[node] | nodeToNeigh[neigh] # add new neighbors to the outer border
                nodeToNeighTillCurLevel[node] = nodeToNeighTillCurLevel[node] | nodeToNeigh[neigh] # add neighbors at distance k to the center node

        EigenListToNode = defaultdict(list)
        for node in nodeToNeighNextLevel.keys():
            #print "Current Node: %d" %(node)
            numNeighs = len(nodeToNeighTillCurLevel[node])
            AdjMat = np.zeros([numNeighs, numNeighs])
            neighList = list(nodeToNeighTillCurLevel[node])
            for i in range(len(neighList)):
                for j in range(len(neighList)):
                    AdjMat[i][j] = GAdjMatrix[neighList[i]][neighList[j]]
            AdjMat = np.mat(AdjMat)
            lamb, _ = LA.eigh(AdjMat)
            #print "Current node's eigenvalue: ", len(lamb)
            eigenValList = list(lamb)
            eigenValList = tuple([round(val, 2) for val in eigenValList])
            EigenListToNode[eigenValList].append(node)

        nodeToNeighCurLevel = {}
        for key in EigenListToNode.keys():
            if len(EigenListToNode[key]) < 2: continue
            else:
                for node in EigenListToNode[key]:
                    nodeToNeighCurLevel[node] = nodeToNeighNextLevel[node]


        curLevel += 1

    print "final level: ", curLevel
    for key, val in nodeToNeighCurLevel.items():
        val_list = sorted(list(val))
        print key, "  ", len(val_list) , " ", val_list
    #print nodeToNeighCurLevel


def detectSymmetry(path):
    numNode = 283
    AdjMat = np.zeros([numNode, numNode])

    f = open(path)
    line = f.readline()
    while line:
        edge = line.split(' ')
        src = int(edge[0])
        dst = int(edge[1])
        #weight = 1
        edge[2] = edge[2][0 : len(edge[2]) - 1]
        weight = int(edge[2])
        weight = 1
        AdjMat[src][dst] = weight
        line = f.readline()
    findKSymmetry(AdjMat)


detectSymmetry("../data/celegans_n283.txt")


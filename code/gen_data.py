import snap


def gen_data():
	graph = snap.GenRndGnm(snap.PNGraph, 300, 2400, True)
	snap.SaveEdgeList(graph, "../data/Erdos-Renyi.txt")
	graph = snap.GenPrefAttach(300, 8)
	snap.SaveEdgeList(graph, "../data/PrefAttach.txt")
	graph = snap.GenRndPowerLaw(300, 1.2)
	snap.SaveEdgeList(graph, "../data/power-law.txt")


if __name__ == '__main__':
	gen_data()
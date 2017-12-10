import csv
import json
from collections import defaultdict

def parseNetworkCsv(path):

    data_file = open(path, 'r')
    neuron_data = [row for row in csv.reader(data_file.read().splitlines())]
    adj_list = defaultdict(list)
    neuron_to_id = {}
    count = 0
    for edge in neuron_data:
        weight = edge[3]
        if weight == 'Nbr':
            continue
        if edge[2] == 'S' or edge[2] == 'Sp':
            # send
            src = edge[0]
            dst = edge[1]
            adj_list[src].append((dst, weight))

        elif edge[2] == 'R' or edge[2] == 'Rp':
            # receive
            src = edge[1]
            dst = edge[0]
            adj_list[src].append((dst, weight))
        else:
            # bi-direction
            src = edge[0]
            dst = edge[1]

            adj_list[src].append((dst, weight))
            adj_list[dst].append((src, weight))

        # map new node to some id
        if src not in neuron_to_id:
            neuron_to_id[src] = count
            count += 1
        if dst not in neuron_to_id:
            neuron_to_id[dst] = count
            count += 1

    mapNeuronToDeg = {}
    for neuron in adj_list:
        mapNeuronToDeg[neuron] = len(adj_list[neuron])
    #print len(adj_list)
    return adj_list, mapNeuronToDeg, neuron_to_id

def parseNetworkTxt(path):
    f = open(path)
    line = f.readline()
    adj_list = defaultdict(list)
    while line:
        edge = line.split('\t')
        src = edge[0]
        dst = edge[1]
        weight = edge[2]
        adj_list[src].append((dst, weight))
        line = f.readline()

    mapNeuronToDeg = {}
    for neuron in adj_list:
        mapNeuronToDeg[neuron] = len(adj_list[neuron])

    return adj_list, mapNeuronToDeg


adj_list_neuron, mapNeuronToDeg, neuron_to_id = parseNetworkCsv('../data/NeuronConnect.csv')
print len(neuron_to_id)
f = open('../data/celegans_n283.txt', 'w')
for neuron, neigh_list in adj_list_neuron.items():
    for neigh in neigh_list:
        edge = [str(neuron_to_id[neuron]), str(neuron_to_id[neigh[0]]), str(neigh[1])]
        f.write(' '.join(edge) + '\n')

f.close()

f = open('../data/map_neuron_to_id.txt', 'w')
f.write(json.dumps(neuron_to_id))
f.close()




#adj_list_id, mapIdToDeg = parseNetworkTxt('../data/celegans_n306.csv')

#neuronToDegList = sorted([(deg, neuron) for neuron, deg in mapNeuronToDeg.items()])[::-1]
#idToDegList = sorted([(deg, id) for id, deg in mapIdToDeg.items()])[::-1]

# print neuronToDegList
# print idToDegList





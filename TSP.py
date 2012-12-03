import sys
import os
import random
import matplotlib.pyplot as plt

# Points are represented as
# {
#   "A":[0.1, 0.3],
#   "B":[0.3, 0.5],
#   etc
# }

def generateTSP(numdatapoints):
    data = {}
    dpname = 'A'
    for i in range(numdatapoints):
        x = random.random()
        y = random.random()
        data[dpname] = (x,y)
        dpname = chr(ord(dpname) + 1)
    return data

def plotTSP(data):
    for key in data:
        pos = data[key]
        dot, = plt.plot(pos[0], pos[1], 'ro', label=key)
        plt.annotate(key, xy=(pos[0], pos[1]+0.02))
    plt.axis([-0.1, 1.1, -0.1, 1.1])

def plotmst(data, mst, col):
    for item in mst:
        p1 = data[item[0]]
        p2 = data[item[1]]
        xs = [p1[0], p2[0]]
        ys = [p1[1], p2[1]]
        line, = plt.plot(xs, ys)
        plt.setp(line, color=col)

def plotsolution(data, soln, col):
    xs = []
    ys = []
    for item in soln:
        positem = data[item]
        xs.append(positem[0])
        ys.append(positem[1])
    line, = plt.plot(xs, ys)
    plt.setp(line, color=col)
    
def dsqr(data, k1, k2):
    p1 = data[k1]
    p2 = data[k2]
    ds = pow(p2[0]-p1[0], 2) + pow(p2[1] - p1[1],2)
    return ds

def dist(data, k1, k2):
    return pow(dsqr(data, k1, k2), 0.5)

def treecost(data, subset, apex):
    cost = 0
    for item in subset:
        if item is not apex:
            cost = cost + dist(data, apex, item)
    return cost


def edge(data, item1, item2):
    if item1 < item2:
        return (item1, item2, dist(data, item1, item2))
    else:
        return (item2, item1, dist(data, item1, item2))

def connected(graph, a, b):
    visited = []
    queue = [a]
    while len(queue) > 0:
        u = queue[0]
        visited.append(u)
        if u == b:
            return True
        queue = queue[1:]
        for item in graph:
            vert = None
            if item[0] == u:
                vert = item[1]
            elif item[1] == u:
                vert = item[0]
            if (vert not in visited) and (vert not in queue):
                queue.append(vert)
    return False

# Kruskal's algorithm
def mst(data, subset):
    graph_edges = []
    for i in subset:
        for j in subset:
            if i is not j:
                e = edge(data, i, j)
                if e not in graph_edges:
                    graph_edges.append(e)
    # Sort graph edges by cost
    graph_edges = sorted(graph_edges, key = lambda edge : edge[2])
    subset = []
    for e in graph_edges:
        if not connected(subset, e[0], e[1]):
            subset.append(e)
    return subset

def costmst(mst):
    cost = 0
    for item in mst:
        cost = cost + item[2]
    return cost

def nearestneighbor(data, startnode):
    unvisited = set(data.keys())
    visited = set()
    tour = [startnode]
    cpos = startnode
    unvisited.remove(startnode)
    while len(unvisited) > 0:
        nn = None
        mindist = 0
        # Find nearest neighbor
        for item in unvisited:
            if nn is None:
                nn = item
                mindist = dsqr(data, cpos, item)
            else:
                thisdist = dsqr(data, cpos, item)
                if thisdist < mindist:
                    mindist = thisdist
                    nn = item
        # Set curpos to nn, remove nn from unvisited
        tour.append(nn)
        unvisited.remove(nn)
        visited.add(nn)
        cpos = nn
    tour.append(startnode)
    return tour

def tourcost(data, tour):
    if len(tour) <= 1:
        return 0
    cost = 0
    cpos = tour[0]
    tour = tour[1:]
    for item in tour:
        cost = cost + dist(data, cpos, item)
        cpos = item
    return cost

def astarcost(data, tour):
    g = tourcost(data, tour)
    h = costmst(mst(data, get_remaining(data, tour) + tour[:1]))
    return g + h

def get_remaining(data, tour):
    subset = data.keys()
    for item in tour:
        subset.remove(item)
    return subset

def cons_candidates(data, tour):
    candidates = []
    unvisited = get_remaining(data, tour)
    for item in unvisited:
        tc = tour + [item]
        candidates.append(tc)
    return candidates

def astar(data, startnode, stepthru=False):
    tour = [startnode]
    candidate_list = cons_candidates(data, tour)

    while len(candidate_list) > 0:
        # print candidate_list
        # find minimum cost
        mincandidate = None
        mincost = -1
        for item in candidate_list:
            if stepthru:
                print "Mincost: " + str(mincost)
                print item
                print tourcost(data, item)
                print astarcost(data, item)
            if mincandidate == None:
                mincandidate = item
                mincost = astarcost(data, item)
            else:
                thiscost = astarcost(data, item)
                if thiscost < mincost:
                    mincandidate = item
                    mincost = thiscost
        if len(mincandidate) == len(data.keys()):
            # We are done
            return mincandidate + tour
        else:
            if stepthru:
                print "Picked candidate " + str(mincandidate)
                raw_input("Press any key to continue")
            candidate_list.remove(mincandidate)
            candidate_list = candidate_list + cons_candidates(data, mincandidate)
    return None
            
    
if __name__ == "__main__":
    d = generateTSP(8)
    #print d
    plotTSP(d)
    nnsol = nearestneighbor(d, 'A')
    astsol = astar(d, 'A', False)
    plotsolution(d, astsol, 'r')
    f = mst(d, d.keys())
    #print f
    #plotmst(d, f, 'g')
    #plotsolution(d, nnsol, 'b')
    #print tourcost(d, nnsol)
    #print astarcost(d, nnsol[:-1])
    #print tourcost(d, astsol)
    #print astarcost(d, astsol[:-1])
    #print mst(d, d.keys())
    plt.show()

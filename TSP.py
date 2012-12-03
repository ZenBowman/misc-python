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
    

def domapping(m, i):
    while m.has_key(i):
        i = m[i]
    return i

def partially_mapped_crossover(tour1, tour2):
    newtour = []
    cutpoint1 = random.randint(1, len(tour1)/2)
    cutpoint2 = cutpoint1 + len(tour1)/2 - 1
    print cutpoint1
    print cutpoint2

    m = {}
    for j in range(cutpoint1, cutpoint2):
        m[tour2[j]] = tour1[j]
    print m

    newtour.append(domapping(m, tour1[0]))


    for i in range(1, len(tour1)-1):
        if (i >= cutpoint1) and (i < cutpoint2):
            newtour.append(tour2[i])
        else:
            newtour.append(domapping(m,tour1[i]))

    newtour.append(newtour[0])
    return newtour

if __name__ == "__main__":
    d = generateTSP(8)
    #print d
    plotTSP(d)

    i = raw_input("Choose (1) for nearest neighbor, (2) for A-star, (3) to see the MST, and (4) for genetic algorithm")
    nnsol = nearestneighbor(d, 'A')
    astsol = astar(d, 'A', False)
    f = mst(d, d.keys())
    if i == "1":
        plotsolution(d, nnsol, 'b')
    elif i == "2":
        plotsolution(d, astsol, 'r')
    elif i == "3":
        plotmst(d, f, 'g')
    elif i == "4":
        a1 = [1,2,3,4,5,6,7,8,1]
        a2 = [3,7,5,1,6,8,2,4,3]
        print a1
        print a2
        print partially_mapped_crossover(a1, a2)
    #plt.title("Traveling salesman")
    #plt.show()

    

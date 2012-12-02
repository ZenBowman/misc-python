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

def plotsolution(data, soln):
    xs = []
    ys = []
    for item in soln:
        positem = data[item]
        xs.append(positem[0])
        ys.append(positem[1])
    plt.plot(xs, ys)
    
def dsqr(data, k1, k2):
    p1 = data[k1]
    p2 = data[k2]
    ds = pow(p2[0]-p1[0], 2) + pow(p2[1] - p1[1],2)
    return ds

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
        

if __name__ == "__main__":
    d = generateTSP(8)
    print d
    plotTSP(d)
    nnsol = nearestneighbor(d, 'A') 
    plotsolution(d,nnsol)
    plt.show()

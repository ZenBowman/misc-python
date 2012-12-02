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
    


if __name__ == "__main__":
    d = generateTSP(8)
    print d
    plotTSP(d)
    plotsolution(d, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'A'])
    plt.show()

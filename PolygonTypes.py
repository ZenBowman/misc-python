import random
import math

MINEDGESIZE = 0.75
MAXEDGESIZE = 2

def pointToLineDistance(a, b, p):
    normalLength = math.hypot(b.x - a.x, b.y - a.y);
    return abs((p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x)) / normalLength


def lineClosestToPoint(lines, point):
    mindist = 9999
    index = -1
    for i in range(len(lines)):
        l = lines[i]
        dist = pointToLineDistance(l.origin, l.end, point)
        if dist < mindist:
            dist = mindist
            index = i
    return i, lines[i]

def createPointWithinRange(point, mindistance, maxdistance):
    xopt1 = random.uniform(point.x-maxdistance, point.x-mindistance)
    xopt2 = random.uniform(point.x+mindistance, point.x+maxdistance)
    yopt1 = random.uniform(point.y-mindistance, point.y-mindistance)
    yopt2 = random.uniform(point.y+mindistance, point.y+maxdistance)

    xr = random.choice([1,2])
    xval = xopt1
    if xr == 2:
        xval = xopt2
        
    yr = random.choice([1,2])
    yval = yopt1
    if yr == 2:
        yval = yopt2
    return Point( xval, yval )

def createPointWithinBounds(bounds):
    return Point(random.uniform(bounds.bottomLeft.x, bounds.topRight.x), random.uniform(bounds.bottomLeft.y, bounds.topRight.y))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def squaredDistance(self, other):
        return (self.x-other.x)**2 + (self.y-other.y)**2

class Line:
    def __init__(self, origin, end):
        self.origin = origin
        self.end = end

class Bounds:
    def __init__(self, bottomLeft, topRight):
        self.bottomLeft = bottomLeft
        self.topRight = topRight

class Polygon:
    def sides(self):
        raise Exception("Not implemented!")

class Triangle:
    def __init__(self, bounds):
        self.lines = []
        p1 = createPointWithinBounds(bounds)
        p2 = createPointWithinRange(p1, MINEDGESIZE, MAXEDGESIZE)
        p3 = createPointWithinRange(p2, MINEDGESIZE, MAXEDGESIZE)
        self.lines.append(Line(p1, p2))
        self.lines.append(Line(p2, p3))
        self.lines.append(Line(p3, p1))
        
    def sides(self):
        return self.lines

class Quadrilateral:
    def __init__(self, bounds):
        self.lines = []
        p1 = createPointWithinBounds(bounds)
        p2 = createPointWithinRange(p1, MINEDGESIZE, MAXEDGESIZE)
        p3 = createPointWithinRange(p2, MINEDGESIZE, MAXEDGESIZE)
        p4 = createPointWithinRange(p3, MINEDGESIZE, MAXEDGESIZE)
        tempLines = [Line(p1, p2), Line(p2, p3), Line(p3, p1)]
        closestLineIndex, closestLine = lineClosestToPoint(tempLines, p4)
        tempLines.pop(closestLineIndex)
        l3 = Line(closestLine.origin, p4)
        l4 = Line(closestLine.end, p4)
        self.lines = tempLines
        self.lines.append(l3)
        self.lines.append(l4)

    def sides(self):
        return self.lines


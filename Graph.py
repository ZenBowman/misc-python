
WHITE = "WHITE"
BLACK = "BLACK"
GREY = "GREY"
TIME = 0

class Vertex:
    def __init__(self, key):
        self.key = key
        self.adjlist = {}

    def display(self):
        print "Key = %s\tEdges = %s" % (self.key, str(self.adjlist.keys()))

    def __repr__(self):
        return "%s: %s" % (str(self.key), str(self.adjlist.keys()))

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, key):
        self.vertices[key] = Vertex(key)

    def add_directed_edge(self, fromv, tov, weight):
        self.vertices[fromv].adjlist[tov] = weight

    def add_undirected_edge(self, fromv, tov, weight):
        self.add_directed_edge(fromv, tov, weight)
        self.add_directed_edge(tov, fromv, weight)
        
    def create(self):
        print "Graph creation helper"
        directed = False
        directedq = raw_input("Is this a directed graph (y or n)?")
        if directedq.lower() == 'y':
            directed = True
        while 1:
            v = raw_input("Enter Vertex key, hit 'q' when finished:\t")
            if v=='q':
                break
            self.add_vertex(v)

        while 1:
            s = raw_input("Starting vertex ('q' to exit):\t")
            if (s == 'q'):
                break
            e = raw_input("Ending vertex:\t")
            if directed:
                self.add_directed_edge(s,e,1)
            else:
                self.add_undirected_edge(s,e,1)
                
    def display(self):
        for vert in self.vertices.values():
            vert.display()

    def dfs_visit(self, vert, verbose, list):
        global TIME
        TIME += 1
        vert.d = TIME
        vert.color = GREY
        for v in vert.adjlist.keys():
            u = self.vertices[v]
            if u.color == WHITE:
                u.parent = vert
                list = self.dfs_visit(u, verbose, list)
        vert.color = BLACK
        list.append(vert)
        if verbose:
            print "Visited " + str(vert.key)        
        TIME += 1
        vert.f = TIME
        return list

    def dfs(self, verbose):
        global TIME
        list = []
        for vert in self.vertices.values():
            vert.color = WHITE
            vert.parent = None
            vert.d = -1
            vert.f = -1
        TIME = 0
        for vert in self.vertices.values():
            if vert.color == WHITE:
                list = self.dfs_visit(vert, verbose, list)
        return list

    def bfs(self, vertex, target):
        visited = []
        self.vertices[vertex].d = 0
        queue = [self.vertices[vertex]]
        d = 0
        
        while len(queue) > 0:
            u = queue[0]
            visited.append(u)
            if u.key == target:
                return (u, d)
            queue = queue[1:]
            for v in u.adjlist.keys():
                vert = self.vertices[v]
                if ((vert not in visited) and (vert not in queue)):
                    print "Adding %s to queue" % vert
                    queue.append(vert)
            d += 1


if __name__ == "__main__":
    g = Graph()
    g.create()
    g.display()
    #print g.bfs('1','3')
    print g.dfs(True)

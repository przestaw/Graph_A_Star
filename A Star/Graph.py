class Neighbour:
    def __init__(self, id, distance):
        self.distance = distance
        self.id = id


class Link:
    def __init__(self, source, target, distance):
        self.source = source
        self.target = target
        self.distance = distance


class Node:
    def __init__(self, idnum, id, corX, corY):
        self.idnum = idnum
        self.id = id
        self.x = corX
        self.y = corY
        self.adjacent = []
        self.costs = {}

    def add_neighbour(self, neighbour):
        self.adjacent.append(neighbour)
        self.costs[neighbour.id] = neighbour.distance

    def cost(self, nodeId):
        return self.costs[nodeId]


class Network:
    def __init__(self):
        self.Nodes = {}

    def addNode(self, node):
        self.Nodes[node.id] = node

    def addLink(self, link):
        self.Nodes[link.target].add_neighbour(Neighbour(link.source, link.distance))
        self.Nodes[link.source].add_neighbour(Neighbour(link.target, link.distance))

    def getNode(self, nodeId):
        return self.Nodes[nodeId]

    def neighbors(self, node):
        return self.Nodes[node].adjacent


class Path:
    def __init__(self):
        self.nodes = []

    def __str__(self):
        ret = "Path distance: " + str(self.distance()) + "\n "
        first = True
        for i in self.nodes:
            if first:
                first = False
                ret += str(i.id)
            else:
                ret += " -> " + str(i.id)
        return ret

    def distance(self):
        total = 0
        prev = 0
        if len(self.nodes) == 0:
            return -1
        for i in self.nodes:
            if prev == 0:
                prev = i
            else:
                total += prev.cost(i.id)
                prev = i
        return total

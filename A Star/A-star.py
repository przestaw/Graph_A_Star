import xml.etree.cElementTree as ElementTree
import xml.dom.minidom as minidom
import math
import sys
from Queue import Queue
from Queue import PriorityQueue
from Graph import *

def loadGraph(inputFile):
    MyNetwork = Network()
    try:
        graph = ElementTree.parse(inputFile)
        root = graph.getroot()

        for node in root.iter('node'):
            MyNetwork.addNode(Node(node.get('id'), float(node.find('coordinates').find('x').text), float(node.find('coordinates').find('y').text)))

        for link in root.iter('link'):
            source = link.find('source').text
            target = link.find('target').text
            dist = float(link.find('distance').text)

            MyNetwork.addLink(Link(source , target, dist))

        return MyNetwork
    except FileNotFoundError:
        print("Input file not found")

def heuristic(curr, goal):
    x1 = curr.x
    y1 = curr.y
    x2 = goal.x
    y2 = goal.y

    disX = abs(x1-x2)
    disY = abs(y1-y2)
    return math.sqrt((disX*disX)+(disY*disY))/2

def reconstructPath(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def aStarSearch(network, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start.id: None}
    cost_so_far = {start.id: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            return came_from

        for iter in network.neighbors(current.id):
            next = network.getNode(iter.id)
            new_cost = cost_so_far[current.id] + iter.distance
            if next not in cost_so_far or new_cost < cost_so_far[next.id]:
                cost_so_far[next.id] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next.id] = current.id

    return {}

if __name__ == "__main__":
    MyNetwork = loadGraph(sys.argv[1])

    result = aStarSearch(MyNetwork, MyNetwork.getNode("Gdansk"), MyNetwork.getNode("Poznan"))
    print(result)
    path = reconstructPath(result, MyNetwork.getNode("Gdansk").id, MyNetwork.getNode("Poznan").id)
    print(path)
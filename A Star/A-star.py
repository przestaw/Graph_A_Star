from Graph import *
from Queue import *
import xml.etree.cElementTree as ElementTree
import xml.dom.minidom as minidom
import math
import sys
sys.path.append('..')
import distances
import time


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
        return MyNetwork

def heuristic(curr, goal):
    return distances.haversine((curr.y, curr.x), (goal.y, goal.x))

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

    startTime = time.perf_counter()

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break;

        for iter in network.neighbors(current.id):
            next = network.getNode(iter.id)
            new_cost = cost_so_far[current.id] + iter.distance
            if next.id not in cost_so_far or new_cost < cost_so_far[next.id]:
                cost_so_far[next.id] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next.id] = current.id

    endTime = time.perf_counter()
    return came_from, cost_so_far[goal.id], endTime - startTime

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Provide all arguments : <input file> <source> <target>")
    elif sys.argv[2] == sys.argv[3]:
        print("Source must be diffrent from target")
    else:
        source = sys.argv[2]
        target = sys.argv[3]

        MyNetwork = loadGraph(sys.argv[1])
        if not MyNetwork.empty():
            try:
                result, distance, time = aStarSearch(MyNetwork, MyNetwork.getNode(source), MyNetwork.getNode(target))
                path = reconstructPath(result, source, target)
                print(path, "\nDistance : ", distance, "\nTime : ", time, " sec")
            except KeyError as error:
                print("Entered bad city name :", error.args[0], "\nPlease provide correct name")
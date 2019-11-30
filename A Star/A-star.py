import xml.etree.cElementTree as ElementTree
import sys
import time
sys.path.append('..')
import distances
from copy import copy
from Queue import PriorityQueue
from Graph import *


def load_graph(input_file):
    my_network = Network()
    try:
        graph = ElementTree.parse(input_file)
        root = graph.getroot()
        next_idnum = 0
        for node in root.iter('node'):
            my_network.addNode(Node(next_idnum, node.get('id'), float(node.find('coordinates').find('x').text),
                                    float(node.find('coordinates').find('y').text)))
            next_idnum += 1
        for link in root.iter('link'):
            source_node = link.find('source').text
            target_node = link.find('target').text
            dist = float(link.find('distance').text)

            my_network.addLink(Link(source_node, target_node, dist))

        return my_network
    except FileNotFoundError:
        print("Input file not found")


def heuristic(curr, goal):
    return distances.haversine((curr.y, curr.x), (goal.y, goal.x))


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star_search(network, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start.id: None}
    cost_so_far = {start.id: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            return came_from

        for i in network.neighbors(current.id):
            next_node = network.getNode(i.id)
            new_cost = cost_so_far[current.id] + i.distance
            if next_node.id not in cost_so_far or new_cost < cost_so_far[next_node.id]:
                cost_so_far[next_node.id] = new_cost
                priority = new_cost + heuristic(next_node, goal)
                frontier.put(next_node, priority)
                came_from[next_node.id] = current.id

    return {}


def brute_force_util(network, start, goal, visited, path, best_path):
    visited[start.idnum] = True
    path.nodes.append(start)
    if start.idnum == goal.idnum:
        if best_path.distance() == -1:
            best_path.nodes = copy(path.nodes)
        if best_path.distance() >= path.distance():
            best_path.nodes = copy(path.nodes)
    else:
        for i in network.neighbors(start.id):
            if not visited[network.Nodes[i.id].idnum]:
                brute_force_util(network, network.Nodes[i.id], goal, visited, path, best_path)

    path.nodes.pop()
    visited[start.idnum] = False


def brute_force(network, start, goal):
    visited = [False] * (len(network.Nodes))
    path = Path()
    best_path = Path()

    brute_force_util(network, start, goal, visited, path, best_path)
    return best_path


def nice_path(path):
    ret = ""
    first = True
    for i in path:
        if first:
            first = False
            ret += str(i)
        else:
            ret += " -> " + str(i)
    return ret


def path_distance(network, path):
    total = 0
    prev = 0
    ret = "Path distance: "
    for i in path:
        if prev == 0:
            prev = i
        else:
            total += network.Nodes[prev].cost(i)
            prev = i
    return ret + str(total)


if __name__ == "__main__":
    search_mode = "2"
    if len(sys.argv) == 5:  # user selected search mode
        search_mode = sys.argv[4]
    if len(sys.argv) < 4:
        print("Provide all arguments : <input file> <source> <target> <mode>(optional)\nModes:\n\t"
              "1 - brute force\n\t2 - A* (default)\n\t3 - both")
    elif sys.argv[2] == sys.argv[3]:
        print("Source must be diffrent from target")
    else:
        source = sys.argv[2]
        target = sys.argv[3]

        loaded_network = load_graph(sys.argv[1])

        try:
            source = loaded_network.getNode(source)
            target = loaded_network.getNode(target)
        except KeyError as error:
            print("Entered bad city name: ", error.args[0], "\nPlease provide correct name")

        bf_time = 0
        astar_time = 0

        if search_mode in ("1", "3"):
            startTime = time.perf_counter()
            bf_path = brute_force(loaded_network, source, target)
            endTime = time.perf_counter()
            bf_time = endTime-startTime
            print("Brute force algorithm:\n", bf_path, "\nTime:", bf_time, " sec\n")

        if search_mode in ("2", "3"):
            startTime = time.perf_counter()
            result = a_star_search(loaded_network, source, target)
            astar_path = reconstruct_path(result, source.id, target.id)
            endTime = time.perf_counter()
            astar_time = endTime-startTime
            print("A* algorithm:\n", path_distance(loaded_network, astar_path), "\n", nice_path(astar_path), "\nTime:",
                  astar_time, " sec")

        if search_mode is "3":
            print("\nA* to brute force ratio is", astar_time/bf_time)

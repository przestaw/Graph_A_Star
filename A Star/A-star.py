import xml.etree.cElementTree as ElementTree
import sys
import time
from random import randint

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
    if dijkstra:
        return 0
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


def generate_test_data(network, amount):
    names = []
    for i in network.Nodes:
        names.append(i)
    ret = []
    for i in range(amount):
        s = randint(0, len(names)-1)
        f = s
        while s == f:
            f = randint(0, len(names)-1)
        ret.append((network.Nodes[names[s]], network.Nodes[names[f]]))
    return ret


if __name__ == "__main__":
    search_mode = "2"
    num_tests = None
    if len(sys.argv) < 5 and not (len(sys.argv) == 4):
        print("Provide all arguments : <input file> <mode> <source> <target>\nModes:\n\t"
              "1 - brute force\n\t2 - A* (default)\n\t3 - Dijkstra\n\t4 - A* and Dijkstra \n\t5 - all at once"
              "\n\t6 <number> - run <number> tests for A* and Dijkstra ")
    elif sys.argv[2] != "6" and sys.argv[3] == sys.argv[4]:
        print("Source must be different from target")
    else:
        search_mode = sys.argv[2]
        if search_mode == "6":
            num_tests = int(sys.argv[3])
        else:
            source = sys.argv[3]
            target = sys.argv[4]
        loaded_network = load_graph(sys.argv[1])

        if search_mode != "6":
            try:
                source = loaded_network.getNode(source)
                target = loaded_network.getNode(target)
            except KeyError as error:
                print("Entered bad city name: ", error.args[0], "\nPlease provide correct name")
                exit(-1)

        bf_time = 0
        astar_time = 0
        dijkstra_time = 0
        dijkstra = False

        if search_mode in ("1", "5"):
            startTime = time.perf_counter()
            bf_path = brute_force(loaded_network, source, target)
            endTime = time.perf_counter()
            bf_time = endTime-startTime
            print("Brute force algorithm:\n", bf_path, "\nTime:", bf_time, " sec\n")

        if search_mode in ("2", "4", "5"):
            startTime = time.perf_counter()
            result = a_star_search(loaded_network, source, target)
            endTime = time.perf_counter()
            astar_time = endTime-startTime
            astar_path = reconstruct_path(result, source.id, target.id)
            print("A* algorithm:\n", path_distance(loaded_network, astar_path), "\n", nice_path(astar_path), "\nTime:",
                  astar_time, " sec")

        if search_mode in ("3", "4", "5"):
            dijkstra = True
            startTime = time.perf_counter()
            result = a_star_search(loaded_network, source, target)
            endTime = time.perf_counter()
            dijkstra_time = endTime-startTime
            dijkstra_path = reconstruct_path(result, source.id, target.id)
            print("Dijkstra algorithm:\n", path_distance(loaded_network, dijkstra_path), "\n", nice_path(dijkstra_path), "\nTime:",
                  dijkstra_time, " sec")

        print()

        if search_mode in ("4", "5"):
            print("A* to Dijkstra ratio is", astar_time / dijkstra_time)

        if search_mode is "5":
            print("A* to brute force ratio is", astar_time / bf_time)

        if search_mode is "6":
            test_data = generate_test_data(loaded_network, num_tests)

            startTime = time.perf_counter()
            for i in range(num_tests):
                result = a_star_search(loaded_network, test_data[i][0], test_data[i][1])
            endTime = time.perf_counter()
            astar_time = endTime-startTime

            startTime = time.perf_counter()
            dijkstra = True
            for i in range(num_tests):
                result = a_star_search(loaded_network, test_data[i][0], test_data[i][1])
            endTime = time.perf_counter()
            dijkstra_time = endTime - startTime

            print("Tested", num_tests, "times with random sources and destinations:\n", "A* time:", astar_time,
                  "s\n Dijkstra time:", dijkstra_time, "s\n\n A* to Dijkstra ratio:", astar_time/dijkstra_time)

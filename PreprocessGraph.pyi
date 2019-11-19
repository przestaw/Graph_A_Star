import xml.etree.cElementTree as ElementTree
import xml.dom.minidom as minidom
import math
import sys

class Node:
    def __init__(self, id, corX, corY):
        self.id = id
        self.x = corX
        self.y = corY

class Link:
    def __init__(self, source, target, distance):
        self.source = source
        self.target = target
        self.distance = distance

class NetworkStructure:
    def __init__(self):
        self.Nodes = []
        self.Links = []
    def addNode(self, node):
        self.Nodes.append(node)
    def addLink(self, link):
        self.Links.append(link)
    def getNode(self, nodeId):
        ret = []
        for node in self.Nodes:
            if(node.id == nodeId):
                ret.append(node)
        return ret

def calcDistance(x1, y1, x2, y2):
    disX = abs(x1-x2)
    disY = abs(y1-y2)
    return math.sqrt((disX*disX)+(disY*disY))

def processGraph(inputFile, outputFile):
    MyNetwork = NetworkStructure()
    try:
        graph = ElementTree.parse(inputFile)
        root = graph.getroot()

        for node in root.iter('node'):
            MyNetwork.addNode(Node(node.get('id'), float(node.find('coordinates').find('x').text), float(node.find('coordinates').find('y').text)))

        for link in root.iter('link'):
            sourceText = link.find('source').text
            targetText = link.find('target').text

            source = MyNetwork.getNode(sourceText).pop()
            target = MyNetwork.getNode(targetText).pop()
            dist = calcDistance(source.x, source.y, target.x, target.y)

            MyNetwork.addLink(Link(sourceText , targetText, dist))

        exportXML(MyNetwork, outputFile)
    except FileNotFoundError:
        print("Input file not found")

def exportXML(networkStructure, filename):
    root = ElementTree.Element("network", version="1.0")
    netStructDoc = ElementTree.SubElement(root, "networkStructure")
    nodes = ElementTree.SubElement(netStructDoc, "nodes")
    links = ElementTree.SubElement(netStructDoc, "links")

    for node in networkStructure.Nodes:
        nodeEl = ElementTree.SubElement(nodes, "node", id=node.id)
        coor = ElementTree.SubElement(nodeEl, "coordinates")
        x = ElementTree.SubElement(coor, "x").text = str(node.x)
        y = ElementTree.SubElement(coor, "y").text = str(node.y)

    for link in networkStructure.Links:
        linkEl = ElementTree.SubElement(links, "link")
        source = ElementTree.SubElement(linkEl, "source").text = link.source
        target = ElementTree.SubElement(linkEl, "target").text = link.target
        distance = ElementTree.SubElement(linkEl, "distance").text = str(link.distance)

    tree = ElementTree.ElementTree(root)

    #convert ET to dom
    dom = minidom.parseString(ElementTree.tostring(root, xml_declaration=True))
    try:
        file = open(filename, mode='x')
        dom.writexml(file, indent='', addindent='  ', newl='\n', encoding="utf-8")
        file.close()
    except FileExistsError:
        print("Output file Exists")
    except:
        print("Error during output file creation")




if __name__ == "__main__":
    print("Hello : here is graph professional preprocessor")
    if len(sys.argv) >= 3 :
        processGraph(sys.argv[1], sys.argv[2])
    else:
        print("Provide input and output file")
    # val = 0
    # while val != '2':
    #     val = input("Press 1 to : process graph\nPress 2 to : Exit\n")
    #     if val == '1' :
    #         inputFile = input("Provide input filename : ")
    #         outputFile = input("Provide output filename : ")
    #         processGraph(inputFile, outputFile)
    #     elif val != '2' :
    #         print("Invalid input")
    #     else :
    #         print("Bye, Bye !")


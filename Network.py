from os import system

class Network():

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.types = []
    
    def addNode(self,node):
        self.nodes.append(node)
    
    def addEdge(self,edge):
        self.edges.append(edge)
    
    def addType(self,typ):
        self.types.append(typ)
class Routes():

    def __init__(self):
        self.ids = []
        self.edges = []
        self.count = 0
        self.traffic_lights = []
        self.vehicles_per_route = []
    
    def add(self,id,edges):
        self.ids.append(id)
        self.edges.append(edges)
        self.traffic_lights.append([])
        self.vehicles_per_route.append([])
        self.count+=1
    
    # load routes from file
    def load(self,filename):
        f = open(filename,'r')
        routes = f.readlines()
        for r in routes:
            route = r.split(':')
            self.add(route[0],route[1].replace(',',''))

    def index(self,name):
        return self.ids.index(name)
      
    def build(self,index,f):
        print("<route id=\""+str(self.ids[index])+"\" edges=\""+str(self.edges[index])+"\" />",file=f)
    
    def name(self,index):
        return self.ids[index]
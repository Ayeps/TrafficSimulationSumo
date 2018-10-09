class Routes():

    def __init__(self):
        self.ids = []
        self.edges = []
        self.count = 0
        pass
    
    def add(self,id,edges):
        self.ids.append(id)
        self.edges.append(edges)
        self.count+=1
    
    # load routes from file
    def load(self,filename):
        f = open(filename,'r')
        routes = f.readlines()
        for r in routes:
            route = r.split(':')
            self.ids.append(route[0])
            self.edges.append(route[1].replace(',',''))
            self.count+=1

      
    def build(self,index,f):
        print("<route id=\""+str(self.ids[index])+"\" edges=\""+str(self.edges[index])+"\" />",file=f)
    
    def name(self,index):
        return self.ids[index]
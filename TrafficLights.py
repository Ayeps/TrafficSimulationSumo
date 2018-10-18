import traci

class TrafficLights():

    def __init__(self):
        self.traffic_lights = []
        self.traffic_lights_positions = []
        self.crossings = []
        self.order = []
    
    def add(self,tf,route_cross):
        self.traffic_lights.append(tf)
        self.crossings.append(route_cross)
        self.order.append([])
    
    def getRoutes(self,i):
        return self.crossings[i]

    def index(self,name):
        return self.traffic_lights.index(name)

    def defPositions(self):
        for tf in self.traffic_lights:
            self.traffic_lights_positions.append(traci.junction.getPosition(tf))
    
    def getPosition(self,i):
        return self.traffic_lights_positions[i]
    
    def getPhase(self,tf):
        return traci.trafficlight.getPhase(tf)
    
    def setPhase(self,tf,p):
        traci.trafficlight.setPhase(tf, p)

    def green(self,tf):
        traci.trafficlight.setPhase(tf, 0)
        for x in self.traffic_lights:
            if(x[0]==tf):
                x[1] = 'green'
    
    def yellow(self,tf):
        traci.trafficlight.setPhase(tf, 1)
        for x in self.traffic_lights:
            if(x[0]==tf):
                x[1] = 'yellow'

    def red(self,tf):
        traci.trafficlight.setPhase(tf, 2)
        for x in self.traffic_lights:
            if(x[0]==tf):
                x[1] = 'red'
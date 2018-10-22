import traci

class TrafficLights():

    def __init__(self):
        self.traffic_lights = []
        self.crossings = []
        self.traffic_lights_positions = []
        self.detectors = []
        self.algorighms = []
        self.order = []
        self.signal = []
        self.queues = []
        self.lqfflag = []
    
    def add(self,tf,route_cross,signals,detectors,alg):
        self.traffic_lights.append(tf)
        self.crossings.append(route_cross)
        self.signal.append(signals)
        self.detectors.append(detectors)
        self.algorighms.append(alg)
        self.order.append([])
        self.lqfflag.append(0)
        self.queues.append([ [],[] ])
    
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
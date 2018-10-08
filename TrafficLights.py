import traci

class TrafficLights():

    def __init__(self):
        self.traffic_lights = []
    
    def add(self,tf):
        self.traffic_lights.append([tf,'red'])
    
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
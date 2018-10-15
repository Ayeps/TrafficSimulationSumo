###########################################
##    Autor: Leonardo de Abreu Schmidt   ##
##    Class to manage transit            ##
###########################################

import time

class Manage():

    def __init__(self,detectors,traffic_lights):
        self.intersects = []
        self.detectors = detectors
        self.traffic_lights = traffic_lights
        self.signals = [0]*len(self.traffic_lights.traffic_lights)
        self.time_e = time.time()
    
    def add(self,detectors,traffic_light,traffic_light_algorithm):
        self.intersects.append([detectors,traffic_light,traffic_light_algorithm])

    def zip(self,detector,tf,i):
        
    
    def lqf(self,detector,tf,i):
        idl0 = self.detectors.get(detector[0])
        idl1 = self.detectors.get(detector[1])
        if(idl0>idl1):
            self.signals[i]=2
        elif(idl0<idl1):
            self.signals[i]=0
        
    def signal(self):
        j=0
        for i in self.intersects:
            tf = i[1]
            phase = self.signals[j]
            self.traffic_lights.setPhase(tf, phase)
            j+=1
    
    def run(self,t_time):
        j=0
        if(time.time()-self.time_e>t_time):
            for i in self.intersects:
                detector = i[0]
                tf = i[1]
                alg = i[2]
                if(alg=='lqf'):
                    self.lqf(detector,tf,j)
                elif(alg=='zip'):
                    self.zip(detector,tf,j)
                j+=1
            self.time_e = time.time()
        
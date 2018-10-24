###########################################
##    Autor: Leonardo de Abreu Schmidt   ##
##    Class to manage transit            ##
###########################################

import time
import math
import traci
from os import system as sys

class Manage():

    def __init__(self,detectors,traffic_lights,vehicles,routes):
        self.detectors = detectors
        self.traffic_lights = traffic_lights
        self.vehicles = vehicles
        self.routes = routes
        self.signals = [0]*len(self.traffic_lights.traffic_lights)
        self.time_e = time.time()
        self.running_vehicles = []
        self.step = 0

    def zip(self,detector,tf,i):
        index = self.traffic_lights.index(tf)
        cars = traci.inductionloop.getLastStepVehicleNumber(detector[0])
        cars1 = traci.inductionloop.getLastStepVehicleNumber(detector[1])
        if cars1 > cars:
            if self.signals[index] == 0:
                self.signals[index] = 2
        if cars > cars1:
            if self.signals[index] == 2:
                self.signals[index] = 0
    
    # longest queue first
    def lqf(self,detector,tf,i):
        index = self.traffic_lights.index(tf)
        cross = self.traffic_lights.crossings[index]

        letra = detector[0][0]
        idl0=0
        idl1=0
        for x in detector:
            if(x[0] == letra):
                idl0+=self.detectors.get(x)
            else:
                idl1+=self.detectors.get(x)

        '''lr0 = traci.lanearea.getLastStepVehicleIDs(detector[0])
        lr1 = traci.lanearea.getLastStepVehicleIDs(detector[1])

        if(len(lr0)>0):
            r0 = self.vehicles.route(lr0[0])
        if(len(lr1)>0):
            r1 = self.vehicles.route(lr1[0])'''

        if(self.traffic_lights.lqfflag[index]==0):
            if(idl0>idl1):
                self.signals[index]=self.traffic_lights.signal[index][0]
            elif(idl0<idl1):
                self.signals[index]=self.traffic_lights.signal[index][1]
            self.traffic_lights.lqfflag[index]=1
        else:
            self.traffic_lights.lqfflag[index]=0
            if(self.signals[index]==0):
                self.signals[index]=2
            elif(self.signals[index]==2):
                self.signals[index]=0
    
    # arrival time at traffic light
    def ffat(self,detector,tf,i):
        index = self.traffic_lights.index(tf)
        order = self.traffic_lights.order[index]
        if(len(order)>0):
            ids = []
            for x in detector:
                ids.extend(traci.lanearea.getLastStepVehicleIDs(x))
            for x in order:
                if(x[3]==1 and x[0] not in ids):
                    x[3]=2
                elif(x[3]==0 and (x[0] in ids)):
                    x[3] = 1
            order2 = order.copy()
            for x in order2:
                if(x[3]==2):
                    order.remove(x)
            self.traffic_lights.order[index] = order
            cross = self.traffic_lights.crossings[index] # crossings for the i-esima traffic light
            if(len(order)>0):
                first = order[0]
                sig = self.traffic_lights.signal[index]
                if(first[2]==cross[0]):
                    self.signals[index] = sig[0]
                else:
                    self.signals[index] = sig[1]

    def distance(self,p1,p2):
        return math.sqrt(math.pow(p2[0]-p1[0],2)+math.pow(p2[1]-p1[1],2))

    def sec(self,elem):
        return elem[1]

    def order(self,queues):
        for q in queues:
            q.sort(key=self.sec)

    def updateOrderListByTrafficLight(self):
        i=0
        for x in self.traffic_lights.order:
            tf_pos = self.traffic_lights.getPosition(i)
            lista_aux = []
            for y in x:
                k = y.copy()
                pos = self.vehicles.position(k[0])
                k[1] = self.distance(pos,tf_pos)
                lista_aux.append(k)
            self.traffic_lights.order[i] = lista_aux
            i+=1
        self.order(self.traffic_lights.order)

    def clearRoutes(self):
        for x in self.routes.vehicles_per_route:
            x.clear()

    def updateVehiclesRoutes(self):
        running = self.vehicles.all()
        self.clearRoutes()
        for vi in running:
            if(vi not in self.running_vehicles):
                self.running_vehicles.append(vi)
                route = self.vehicles.route(vi)
                index_route = self.routes.index(route)
                self.routes.vehicles_per_route[index_route].append([vi,0,route,0])
        for tf in self.traffic_lights.traffic_lights:
            index_tf = self.traffic_lights.index(tf)
            routes = self.traffic_lights.getRoutes(index_tf)
            ir0 = self.routes.index(routes[0])
            ir1 = self.routes.index(routes[1])
            insertion_list = self.routes.vehicles_per_route[ir0] + self.routes.vehicles_per_route[ir1]
            for x in insertion_list:
                self.traffic_lights.order[index_tf].append(x)
        self.updateOrderListByTrafficLight()

    def show(self):
        i=0
        for tf in self.traffic_lights.order:
            print(self.traffic_lights.traffic_lights[i])
            for x in tf:
                print(x)
            i+=1

    def signal(self):
        j=0
        for tf in self.traffic_lights.traffic_lights:
            phase = self.signals[j]
            self.traffic_lights.setPhase(tf, phase)
            j+=1
    
    def run(self,t_time,steps,cheating_rate=0):
        i=0
        if(time.time()-self.time_e>t_time):
            for tf in self.traffic_lights.traffic_lights:
                detector = self.traffic_lights.detectors[i]
                alg = self.traffic_lights.algorighms[i]
                if(alg=='lqf'):
                    self.lqf(detector,tf,i)
                elif(alg=='zip'):
                    self.zip(detector,tf,i)
                elif(alg=='ffat'):
                    self.ffat(detector,tf,i)
                i+=1
            self.time_e = time.time()
            self.step = steps
        
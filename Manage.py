###########################################
##    Autor: Leonardo de Abreu Schmidt   ##
##    Class to manage transit            ##
###########################################

import time
import math

class Manage():

    def __init__(self,detectors,traffic_lights,vehicles,routes):
        self.intersects = []
        self.detectors = detectors
        self.traffic_lights = traffic_lights
        self.vehicles = vehicles
        self.routes = routes
        self.signals = [0]*len(self.traffic_lights.traffic_lights)
        self.time_e = time.time()
        self.running_vehicles = []
        self.step = 0
    
    def add(self,detectors,traffic_light,traffic_light_algorithm):
        self.intersects.append([detectors,traffic_light,traffic_light_algorithm])

    def zip(self,detector,tf,i):
        phase = self.traffic_lights.getPhase(tf)
        index = self.traffic_lights.index(tf)
        if(phase==0):
            self.signals[index]=2
        else:
            self.signals[index]=0
    
    # longest queue first
    def lqf(self,detector,tf,i):
        idl0 = self.detectors.get(detector[0])
        idl1 = self.detectors.get(detector[1])
        if(idl0>idl1):
            self.signals[i]=2
        elif(idl0<idl1):
            self.signals[i]=0
    
    # arrival time at traffic light
    def attl(self,detector,tf,i):
        order = self.traffic_lights.order[i]
        if(len(order)>0):
            cross = self.traffic_lights.crossings[i] # crossings for the i-esima traffic light
            first = order[0]
            if(first[2]==cross[0]):
                self.signals[i] = 0
            else:
                self.signals[i] = 2

    def distance(self,p1,p2):
        return math.sqrt(math.pow(p2[0]-p1[0],2)+math.pow(p2[1]-p1[1],2))

    def sec(self,elem):
        return elem[1]

    def order(self,queues):
        for q in queues:
            q.sort(key=self.sec)

    def insert_order(self,elem,lista):
        i=0
        lista_aux = []
        b=False
        if(len(lista)==0):
            lista_aux.append(elem)
        else:
            for x in lista:
                if(elem[1]<x[1] and not b):
                    lista_aux.append(elem)
                    lista_aux.append(x)
                    b=True
                else:
                    lista_aux.append(x)
            if(not b):
                lista_aux.append(elem)
        return lista_aux

    def updateOrderListByTrafficLight(self):
        i=0
        for x in self.traffic_lights.order:
            for y in x:
                tf_pos = self.traffic_lights.getPosition(i)
                pos = self.vehicles.position(y[0])
                vel = self.vehicles.speed(y[0])
                y[1] = self.distance(pos,tf_pos)
            i+=1

    def updateVehiclesRoutes(self):
        self.updateOrderListByTrafficLight()
        vehicles_ids = self.vehicles.all() # all vehicles in the simulation
        temp = []
        for x in self.routes.vehicles_per_route:
            x.clear()
        for vi in vehicles_ids:
            if(vi not in self.running_vehicles):
                self.running_vehicles.append(vi)
                id_route = self.vehicles.route(vi)
                index_route = self.routes.index(id_route)
                self.routes.vehicles_per_route[index_route].append([vi,0,id_route])
        for tf in self.traffic_lights.traffic_lights:
            tf_index = self.traffic_lights.index(tf)
            routes = self.traffic_lights.getRoutes(tf_index)
            ir0 = self.routes.index(routes[0])
            ir1 = self.routes.index(routes[1])
            vr0 = self.routes.vehicles_per_route[ir0]
            vr1 = self.routes.vehicles_per_route[ir1]
            order_list = self.traffic_lights.order[tf_index]
            insertion_list = vr0+vr1
            tf_pos = self.traffic_lights.getPosition(tf_index)
            for x in insertion_list:
                pos = self.vehicles.position(x[0])
                vel = self.vehicles.speed(x[0])
                x[1] = self.distance(pos,tf_pos)
                order_list = self.insert_order(x,order_list)
            self.traffic_lights.order[tf_index] = order_list
        self.show()
        input()
        print("\n\n")

    def show(self):
        for tf in self.traffic_lights.order:
            for x in tf:
                print(x)

    def signal(self):
        j=0
        for i in self.intersects:
            tf = i[1]
            phase = self.signals[j]
            self.traffic_lights.setPhase(tf, phase)
            j+=1
    
    def run(self,t_time,steps):
        j=0
        self.updateVehiclesRoutes()
        #if(time.time()-self.time_e>t_time and steps-self.step==2):
        if(time.time()-self.time_e>t_time):
            for i in self.intersects:
                detector = i[0]
                tf = i[1]
                alg = i[2]
                if(alg=='lqf'):
                    self.lqf(detector,tf,j)
                elif(alg=='zip'):
                    self.zip(detector,tf,j)
                elif(alg=='attl'):
                    self.attl(detector,tf,j)
                j+=1
            self.time_e = time.time()
            self.step = steps
        
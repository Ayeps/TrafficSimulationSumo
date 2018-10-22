###########################################
##    Autor: Leonardo de Abreu Schmidt   ##
##    Class to generate flow             ##
###########################################

from Vehicle import Vehicle
import random

class Flow():

    def __init__(self,number_vehicles,filename,flowroutesfile,intensity=1):
        self.number_vehicles = number_vehicles
        self.filename = filename
        self.routes = open(self.filename, "w")
        self.intensity = intensity
        f = open(flowroutesfile,'r')
        self.lines = f.readlines()
        for l in range(len(self.lines)):
            self.lines[l] = self.lines[l].replace('\n','')
        print(self.lines)
    
    def sec(self,elem):
        return elem[1]

    def generate(self,vehicle,route):
        print("<routes>",file=self.routes)
        vehicle.plan(self.routes)
        ant=0
        for i in range(route.count):
            route.build(i,self.routes)
        i=0
        self.depart = []
        while i<self.number_vehicles:
            temp = []
            for r in range(len(self.lines)):
                t = random.randint(0,self.intensity)
                temp.append([i,t+ant,r])
                i+=1
            ant+=t+self.intensity
            temp.sort(key=self.sec)
            self.depart.extend(temp)
        for v in self.depart:
            vehicle.build(v[0],self.lines[v[2]],v[1],self.routes)
        print("</routes>", file=self.routes)
        self.routes.close()

    '''def generate(self,vehicle,route):
        print("<routes>",file=self.routes)
        vehicle.plan(self.routes)
        ant=0
        for i in range(route.count):
            route.build(i,self.routes)
        for i in range(self.number_vehicles):
            rc = random.randint(0,len(self.lines)-1)
            t = random.randint(0,self.intensity)
            #vehicle.build(i,route.name(rc),t+ant,self.routes)
            #vehicle.build(i,"routevenancio",t+ant,self.routes)
            vehicle.build(i,self.lines[rc],t+ant,self.routes)
            ant+=t+1
        print("</routes>", file=self.routes)
        self.routes.close()'''
###########################################
##    Autor: Leonardo de Abreu Schmidt   ##
##    Class to generate flow             ##
###########################################

from Vehicle import Vehicle
import random

class Flow():

    def __init__(self,number_vehicles,filename,intensity=1):
        self.number_vehicles = number_vehicles
        self.filename = filename
        self.routes = open(self.filename, "w")
        self.intensity = intensity
    
    def generate(self,vehicle,route):
        print("<routes>",file=self.routes)
        vehicle.plan(self.routes)
        ant=0
        for i in range(route.count):
            route.build(i,self.routes)
        for i in range(self.number_vehicles):
            rc = random.randint(0,route.count-1)
            t = random.randint(0,self.intensity)
            vehicle.build(i,route.name(rc),t+ant,self.routes)
            ant+=t+1
        print("</routes>", file=self.routes)
        self.routes.close()
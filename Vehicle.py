###########################################
##    Autor: Leonardo de Abreu Schmidt   ##
##    Class to generate vehicles         ##
###########################################

import traci

class Vehicle():

    def __init__(self,type_v='Car',length=2.0,accel=1.0, decel=5.0,maxSpeed=100.0):
        self.type = type_v
        self.length = length
        self.accel = accel
        self.decel = decel
        self.maxSpeed = maxSpeed
    
    def all(self):
        return traci.vehicle.getIDList()
    
    def route(self,id):
        return traci.vehicle.getRouteID(id)
    
    def position(self,id):
        return traci.vehicle.getPosition(id)

    def speed(self,id):
        return traci.vehicle.getSpeed(id)

    # make the type of an vehicle
    def plan(self,f):
        print("<vType accel=\""+str(self.accel)+"\" decel=\""+str(self.decel)+"\" id=\""+str(self.type)+"\" length=\""+str(self.length)+"\" maxSpeed=\""+str(self.maxSpeed)+"\" sigma=\"0.0\" />",file=f)
    
    # build the vehicle
    def build(self,id,route,depart,f):
        if(id==0):
            print("<vehicle id=\""+str(id)+"\" type=\""+str(self.type)+"\" route=\""+str(route)+"\" depart=\""+str(depart)+"\" color=\"1,0,0\" />",file=f)
        else:
            print("<vehicle id=\""+str(id)+"\" type=\""+str(self.type)+"\" route=\""+str(route)+"\" depart=\""+str(depart)+"\" />",file=f)
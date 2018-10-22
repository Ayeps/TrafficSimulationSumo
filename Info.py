###########################################
##    Autor: Leonardo de Abreu Schmidt   ##
##    Class to get info from simulation  ##
###########################################

import traci
import pickle

class Info():

    def __init__(self,vehicles):
        self.steps = []
        self.vehicles = vehicles
        self.globalWaitingTimes = []
        self.globalRunningVehicles = []
    
    def take(self,step,jump):
        if(step%jump==0):
            self.steps.append(step)
            self.vehicle_ids = self.vehicles.all()
            self.global_waiting_time()
            self.global_running_vehicles()

    def save(self,filename):
        f = open(filename,'wb')
        pickle.dump([self.steps,self.globalWaitingTimes],f)
        f.close()

    def global_running_vehicles(self):
        self.globalRunningVehicles.append(len(self.vehicle_ids))

    def global_waiting_time(self):
        t=0.0
        for v in self.vehicle_ids:
            t+=traci.vehicle.getWaitingTime(v)
        s = len(self.vehicle_ids)
        if(s>0):
            t/=s
        self.globalWaitingTimes.append(t)

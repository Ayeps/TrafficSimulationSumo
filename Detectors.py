import traci

class Detectors():

    def __init__(self):
        self.detectors = []
    
    def add(self,detector):
        self.detectors.append(detector)
    
    def get(self,detector):
        return traci.lanearea.getLastStepVehicleNumber(detector)
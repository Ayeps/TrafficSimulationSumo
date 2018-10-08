from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import subprocess
import time
import includes
import traci
from sumolib import checkBinary

from Flow import Flow
from Vehicle import Vehicle
from Routes import Routes
from TrafficLights import TrafficLights
from Network import Network

flow = Flow(50,"dat/routes.rou.xml")
v = Vehicle()
r = Routes()
tfs = TrafficLights()

r.add("route0","1to2 2to3")
r.add("route1","4to2 2to5")

tfs.add("n2")
tfs.add("n3")

def run():
    step = 0
    tfs.setPhase("n2",2)
    phase=2
    t = time.time()
    idl0 = traci.lanearea.getLastStepVehicleNumber("idl0")
    idl1 = traci.lanearea.getLastStepVehicleNumber("idl1")
    while True:
        if(time.time()-t>1):
            idl0 = traci.lanearea.getLastStepVehicleNumber("idl0")
            idl1 = traci.lanearea.getLastStepVehicleNumber("idl1")
            t=time.time()
        if(idl0>idl1):
            phase=2
        else:
            phase=0
        tfs.setPhase("n2", phase)
        traci.simulationStep()
        step += 1
    traci.close()
    sys.stdout.flush()

if __name__ == "__main__":
    options = includes.get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    flow.generate(v,r)
    traci.start([sumoBinary, "-c", "dat/config.sumocfg"])
    run()
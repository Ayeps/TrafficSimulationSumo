# lqf: delay = 1
# attl: delay = 0.01

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
from Manage import Manage
from Detectors import Detectors
from Info import Info

vehicle_number = 100

flow = Flow(vehicle_number,"datsm/routes.rou.xml",'datsm/flowroutes.txt',intensity=1)
v = Vehicle(length=4)
r = Routes()

info = Info(v)

det = Detectors()
tfs = TrafficLights()

r.load('datsm/rotas.txt')

global_algorithm = "real"

tfs.add("floriano003",["routefloriano","routesilva"],[0,2],["floriano01","silva01"],global_algorithm)

tfs.add("floriano005",["routefloriano","routeandradas"],[0,2],["floriano02","andradas03"],global_algorithm)

tfs.add("floriano008",["routefloriano","routevenancio"],[0,2],["floriano03","venancio02"],global_algorithm)

tfs.add("valandro003",["routevalandro","routevenancio"],[0,2],["venancio01","valandro02"],global_algorithm)

tfs.add("valandro005",["routevalandro","routeandradas"],[2,0],["andradas04","valandro01"],global_algorithm)

mng = Manage(det,tfs,v,r)

def run():
    tfs.defPositions()
    step = 0
    arrived = 0
    while arrived<vehicle_number:
        if(global_algorithm!="real"):
            if(global_algorithm=="attl"):
                mng.updateVehiclesRoutes()
            mng.run(1,step)
            mng.signal()
        info.take(step,5)
        traci.simulationStep()
        step += 1
        arrived+=traci.simulation.getArrivedNumber()
    info.save("info/"+global_algorithm+".info")
    traci.close()
    sys.stdout.flush()
    

if __name__ == "__main__":
    options = includes.get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    flow.generate(v,r)
    traci.start([sumoBinary, "-c", "datsm/config.sumocfg"])
    run()
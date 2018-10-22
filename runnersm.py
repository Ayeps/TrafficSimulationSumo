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

vehicle_number = 100

flow = Flow(vehicle_number,"datsm/routes.rou.xml",'datsm/flowroutes.txt')
v = Vehicle(length=4)
r = Routes()

det = Detectors()
tfs = TrafficLights()

r.load('datsm/rotas.txt')

tfs.add("floriano003",["routefloriano","routesilva"],[0,2],["floriano01","silva01"],'lqf')

tfs.add("floriano005",["routefloriano","routeandradas"],[0,2],["floriano02","andradas03"],'lqf')

tfs.add("floriano008",["routefloriano","routevenancio"],[0,2],["floriano03","venancio02"],'lqf')

tfs.add("valandro003",["routevalandro","routevenancio"],[0,2],["venancio01","valandro02"],'lqf')

tfs.add("valandro005",["routevalandro","routeandradas"],[0,2],["andradas04","valandro01"],'lqf')

mng = Manage(det,tfs,v,r)

def run():
    tfs.defPositions()
    step = 0
    arrived = 0
    while arrived<vehicle_number:
        mng.run(1,step)
        traci.simulationStep()
        step += 1
        mng.signal()
        arrived+=traci.simulation.getArrivedNumber()
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
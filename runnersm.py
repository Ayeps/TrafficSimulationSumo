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

flow = Flow(500,"datsm/routes.rou.xml")
v = Vehicle(length=4)
r = Routes()

det = Detectors()
tfs = TrafficLights()

r.load('datsm/rotas.txt')

'''tfs.add("floriano003",["routefloriano","routesilva"])
tfs.add("floriano005",["routefloriano","routeandradas"])
tfs.add("floriano008",["routefloriano","routevenancio"])'''

tfs.add("valandro003",["routevalandro","routevenancio"])
'''tfs.add("valandro005",["routevalandro","routeandradas"])

tfs.add("riobranco103",["routeriobranco01","routesilva"])
tfs.add("riobranco108",["routeriobranco01","routeandradas"])
tfs.add("riobranco113",["routeriobranco01","routevenancio"])

tfs.add("riobranco012",["routeriobranco02","routevenancio"])
tfs.add("riobranco008",["routeriobranco02","routeandradas"])
tfs.add("riobranco008",["routeriobranco02","routesilva"])'''

mng = Manage(det,tfs,v,r)

#mng.add(["venancio01","valandro02"],"valandro003",'lqf')

mng.add(["il0","il1"],'valandro003','attl')

def run():
    tfs.defPositions()
    step = 0
    while True:
        mng.run(1,step)
        traci.simulationStep()
        step += 1
        mng.signal()
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
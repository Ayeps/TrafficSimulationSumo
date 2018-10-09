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

flow = Flow(150,"dat/routes.rou.xml")
v = Vehicle()
r = Routes()

det = Detectors()
tfs = TrafficLights()

r.add("route0","1to2 2to3 3to6")
r.add("route1","4to2 2to5")
r.add("route2","7to3 3to8")

tfs.add("n2")
tfs.add("n3")

det.add("idl0")
det.add("idl1")
det.add("idl2")
det.add("idl3")

mng = Manage(det,tfs)

mng.add(["idl0","idl1"],"n2",'lqf')
mng.add(["idl2","idl3"],"n3",'lqf')

def run():
    step = 0
    t = time.time()
    while True:
        if(time.time()-t>1):
            mng.run()
        mng.signal()
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
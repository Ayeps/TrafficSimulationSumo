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
v = Vehicle()
r = Routes()

det = Detectors()
tfs = TrafficLights()

#r.add("routefloriano","floriano001tofloriano002 floriano002tofloriano003 floriano003tofloriano004 floriano004tofloriano005 floriano005tofloriano006 floriano006tofloriano007 floriano007tofloriano008 floriano008tofloriano009")

r.load('datsm/rotas.txt')

tfs.add("floriano003")
tfs.add("floriano005")
tfs.add("floriano008")

tfs.add("valandro003")
tfs.add("valandro005")

tfs.add("riobranco103")
tfs.add("riobranco108")
tfs.add("riobranco113")

tfs.add("riobranco012")
tfs.add("riobranco008")

mng = Manage(det,tfs)

mng.add(["venancio01","valandro02"],"valandro003",'lqf')

def run():
    step = 0
    while True:
        mng.run(2)
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
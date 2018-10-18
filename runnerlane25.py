#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random
from Flow import Flow
from Vehicle import Vehicle
from Routes import Routes

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci

flow = Flow(500,"datsm/routes.rou.xml")
v = Vehicle(length=4)
r = Routes()

r.load('datsm/rotas.txt')

# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#    </tlLogic>


def run():
    """execute the TraCI control loop"""
    step = 0
    cars = 0
    cars1 = 0
    
    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("valandro003", 0)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        cars = traci.inductionloop.getLastStepVehicleNumber("il0")
        cars1 = traci.inductionloop.getLastStepVehicleNumber("il1")


        if cars > cars1:
            if traci.trafficlight.getPhase("valandro003")== 0:
                traci.trafficlight.setPhase("valandro003", 1)

        if cars1 >= cars:
            
            if traci.trafficlight.getPhase("valandro003")== 2:
                traci.trafficlight.setPhase("valandro003", 3)


        step += 1
        
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    flow.generate(v,r)

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "datsm/config.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()

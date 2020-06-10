#!/usr/bin/env python3

# **************************************************************************
# * Authors: Tibor Füzik
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <https://www.gnu.org/licenses/>.
# *
# * Copyright (C) 2020 Tibor Füzik
# **************************************************************************

# **************************************************************************
# This is a demo script to show how to control PSD pump or MVP valve through
# python a script, without GUI #
# **************************************************************************

from time import sleep

from hw_classes.mvp_valve import MVPvalve
from hw_classes.psd_pump import PSDpump


# Create a Pump object, with HW adress 1, in Hi res mode, with 15ul syringe installed, communicating on port /dev/ttyUSB0
mypump = PSDpump("PSD/6SF", "0", "/dev/ttyUSB1",True,15)
# Create a MVP object, with HW address 2, the com port is nested with the PSDpump (the same com port - both communicating through same cable)
myvalve = MVPvalve("MVP/4", "1", mypump.com_interface)

# a simple function to wait for the readiness of the devices
def wait_for_readiness(device):
    while not device.get_status()[1]:
        sleep(0.1)

# print out firmware version of our devices
print("PSD firmware: %s" % mypump.get_firmware_version()[3])
wait_for_readiness(mypump)
print("MVP firmware: %s" % myvalve.get_firmware_version()[3])

# Initialize our pump
print("Initializing pump...")
mypump.initialize("right","1")
mypump.run_command()
wait_for_readiness(mypump)

# set pump valve to input position and wait for readiness
print("Moving pump valve to Input...")
mypump.valve_input()
mypump.run_command()
wait_for_readiness(mypump)

# fill the syringe with max speed settings and wait for readiness
print("Filling syringe at max speed...")
mypump.fill_syringe()
mypump.run_command()
wait_for_readiness(mypump)

# initialize the MVP valve and set to to bypass position wait for readiness
print("Initializing MVP valve and moving to Bypass")
myvalve.initialize("left")
myvalve.valve_bypass()
myvalve.run_command()
wait_for_readiness(myvalve)

# create a complex command for the pump, with multiple steps and a loop and run it
print("Running a complex command....")
mypump.valve_output()
mypump.insert_loop_start()
mypump.set_step_position(5000)
mypump.valve_input()
mypump.set_step_position(1000)
mypump.valve_output()
mypump.insert_loop_end(15)
mypump.run_command()

# wait for readiness
wait_for_readiness(mypump)
print("Done.")
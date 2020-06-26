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

from hw_classes.serial_com import Serial_communication


class MVPvalve:
    def __init__(self, hw_type, hw_address, com_port):
        # types:MVP4
        self.hw_type = hw_type
        self.com_port = com_port
        self.hw_address = hw_address

        # check if com port is nested to other device
        if type(self.com_port).__name__ == "Serial_communication":
            self.com_interface = com_port
            self.com_port = self.com_interface.port
        else:
            self.com_interface = Serial_communication(com_port)
            self.com_port = com_port

        self.delay_min = 5
        self.delay_max = 30000
        self.loop_repeat_min = 0
        self.loop_repeat_max = 65535

        self.command_buffer = ""

        self.command_description = {
            "initialize": "initializes the valve output position to the right or left side of the MVP (as viewed from the front of the MVP). [Pump command: Y, Z]",
            "valve_input": "Moves the valve to the input position set by the initialize command. [Pump command: I]",
            "valve_output": "Moves the valve to the output position set by the initialize command. [Pump command: O]",
            "valve_bypass": "Connects the input and output positions, bypassing the syringe. [Pump command B]",
            "valve_extra": "Moves the valve to the extra position (port) relative to the initialize command. [Pump command: E]",
            "insert_loop_start": "Marks a position in a Command String that can be matched with repeat commands. [Pump command: g]",
            "insert_loop_end": "Repeats a command in the command buffer x number of times. [Pump command: G]",
            "delay": "Performs a delay of x milliseconds. [Pump command: M]",
            "halt": "Halts execution of the commands in the command buffer. [Pump command: H]",
            "terminate": "Stops execution of the command buffer. It also aborts the command being executed, except for valve commands. [Pump command: T]",
            "get_command_buffer_status": "Reports the command buffer status. [Pump command: F]",
            "get_firmware_version": "Reports the firmware revision in ASCII. [Pump command: &]",
            "get_mvp_status": "Reports the MVP status. [Pump command: Q]",
            "get_aux1_status": "Reports the Status of the Auxiliary Input 1. [Pump command: ?13]",
            "get_aux2_status": "Reports the Status of the Auxiliary Input 2. [Pump command: ?14]"
        }

    def _send_command(self):
        self.com_interface.send_command(self.command_buffer, self.hw_address)
        self.command_buffer = ""

    def _get_query(self, query_string):
        response = self.com_interface.send_command(query_string, self.hw_address)
        return response

    def run_command(self):
        self.command_buffer += "R"
        return self._send_command()

    def initialize(self, valve):
        if valve == "left":
            self.command_buffer += "Y"
        elif valve == "right":
            self.command_buffer += "Z"
        else:
            return "No initialization command set."
        return "OK"

    def valve_input(self, position=-1):
        if position == -1:
            self.command_buffer += "I"
        else:
            self.command_buffer += "I" + str(position)
        return "OK"

    def valve_output(self, position=-1):
        if position == -1:
            self.command_buffer += "O"
        else:
            self.command_buffer += "O" + str(position)
        return "OK"

    def valve_bypass(self):
        self.command_buffer += "B"
        return "OK"

    def valve_extra(self):
        self.command_buffer += "E"
        return "OK"

    def insert_loop_start(self):
        self.command_buffer += "g"
        return "OK"

    def insert_loop_end(self, repetitions):
        if repetitions >= self.loop_repeat_min and repetitions <= self.loop_repeat_max:
            self.command_buffer += "G" + str(repetitions)
            return "OK"
        else:
            return "Repetitions out of range (%s - %s)" % (self.loop_repeat_min, self.loop_repeat_max)

    def delay(self, delay):
        if delay >= self.delay_min and delay <= self.delay_max:
            self.command_buffer += "M" + str(delay)
            return "OK"
        else:
            return "Delay out of range (%s - %s)" % (self.delay_min, self.delay_max)

    def halt(self, halt_command):
        if halt_command in [0, 1, 2]:
            self.command_buffer += "H" + str(halt_command)
            return "OK"
        else:
            return "Halt command must be 0, 1 or 2"

    def terminate(self):
        self.command_buffer += "T"
        self.run_command()
        return "OK"

    def get_command_buffer_status(self):
        return self._get_query("F")

    def get_firmware_version(self):
        return self._get_query("&")

    def get_status(self):
        return self._get_query("Q")

    def get_aux1_status(self):
        return self._get_query("?13")

    def get_aux2_status(self):
        return self._get_query("?14")

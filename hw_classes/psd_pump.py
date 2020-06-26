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

# TODO remove ugly return OK

from hw_classes.serial_com import Serial_communication


class PSDpump:
    def __init__(self, hw_type, hw_address, com_port, hi_res, syringe_volume):
        # pump_types:PSD/4, PSD/6, PSD/8, STD, SF, HLF, HVT (e.g. define as PSD/4STD, PSD/4SF)
        self.hw_type = hw_type
        self.syringe_volume = float(syringe_volume)
        self.com_port = com_port
        self.hi_res = False
        self.hw_address = hw_address

        # check if com port is nested to other device
        if type(self.com_port).__name__ == "Serial_communication":
            self.com_interface = com_port
            self.com_port = self.com_interface.port
        else:
            self.com_interface = Serial_communication(com_port)
            self.com_port = com_port

        self.command_buffer = ""

        self.load_pump_parameters()

        if hi_res == True:
            self.setHiRes()
        else:
            self.setLoRes()

        self.command_description = {
            "initialize": "Initializes the syringe to the home position and sets valve output position to the right or left side of the PSD (as viewed from the front of the PSD). [Pump command: Y, Z, W]",
            "set_step_position": "Moves the syringe to absolute position x (in steps). [Pump command: A]",
            "reset_syringe_counter_position": "Sets the PSD’s position counter to the value contained in the current encoder position. [Pump command: z]",
            "move_up_steps": "Moves the syringe up x steps. [Pump command: P]",
            "move_down_steps": "Moves the syringe down x steps. [Pump command: D]",
            "set_return_steps": "Sets Return Steps to x steps. [Pump command K]",
            "set_backoff_steps": "Sets Back-off Steps to x steps. [Pump command: k]",
            "valve_input": "Moves the valve to the input position set by the initialize command. [Pump command: I]",
            "valve_output": "Moves the valve to the output position set by the initialize command. [Pump command: O]",
            "valve_bypass": "Connects the input and output positions, bypassing the syringe. [Pump command B]",
            "valve_extra": "Moves the valve to the extra position (port) relative to the initialize command. [Pump command: E]",
            "insert_loop_start": "Marks a position in a Command String that can be matched with repeat commands. [Pump command: g]",
            "insert_loop_end": "Repeats a command in the command buffer x number of times. [Pump command: G]",
            "delay": "Performs a delay of x milliseconds. [Pump command: M]",
            "halt": "Halts execution of the commands in the command buffer. [Pump command: H]",
            "setHiRes": "Enables high resolution mode. [Pump command: N1]",
            "setLoRes": "Enables standard resolution mode. [Pump command: N0]",
            "set_acceleration": "Sets the velocity ramp used by syringe moves to acceleration x. [Pump command: L]",
            "set_start_velocity": "Set start velocity to x motor steps per second. [Pump command: v]",
            "set_max_velocity": "Sets the maximum velocity in motor steps/second. [Pump command: V]",
            "set_syringe_speed": "Sets a predefined syringe maximum velocity. [Pump command: S]",
            "set_stop_velocity": "Sets the stop velocity in motor steps per second. [Pump command: c]",
            "empty_syringe": "Switch to output port, and empty the syringe at given speed.",
            "fill_syringe": "Switch to input port, and empty the syringe at given speed.",
            "move_syringe_up": "Switch to desired port, and move the syringe piston up at given speed.",
            "move_syringe_down": "Switch to desired port, and move the syringe piston down at given speed.",
            "terminate": "Stops execution of the command buffer. It also aborts the command being executed, except for valve commands. [Pump command: T]",
            "get_command_buffer_status": "Reports the command buffer status. [Pump command: F]",
            "get_firmware_version": "Reports the firmware revision in ASCII. [Pump command: &]",
            "get_pump_status": "Reports the pump status. [Pump command: Q]",
            "get_absolute_syringe_position": "Reports the given position of the syringe. [Pump command: ?]",
            "get_start_velocity": "Reports the start velocity in motor steps/second. [Pump command: ?1]",
            "get_max_velocity": "Reports the maximum velocity in motor steps/second. [Pump command: ?2]",
            "get_stop_velocity": "Reports the stop velocity in motor steps/second. [Pump command: ?3]",
            "get_actual_syringe_position": "Reports the actual position of the syringe in steps based on encoder information. [Pump command: ?4]",
            "get_nr_return_steps": "Reports the number of Return Steps. [Pump command: ?12]",
            "get_aux1_status": "Reports the Status of the Auxiliary Input 1. [Pump command: ?13]",
            "get_aux2_status": "Reports the Status of the Auxiliary Input 2. [Pump command: ?14]",
            "get_back_off_steps": "Reports the number of Back-off Steps. [Pump command: ?24]"
        }

    def load_pump_parameters(self):
        if "PSD/4" in self.hw_type:

            self.max_velocity_min = 2
            self.max_velocity_max = 5800
            self.loop_repeat_min = 0
            self.loop_repeat_max = 65535
            self.delay_min = 5
            self.delay_max = 30000
            self.acceleration_min = 0
            self.acceleration_max = 20
            self.start_velocity_min = 50
            self.start_velocity_max = 1000
            self.syringe_speed_preset_min = 1
            self.syringe_speed_preset_max = 40
            self.stop_velocity_min = 50
            self.stop_velocity_max = 2700
            self.syringe_sizes = ["12.5", "25", "50", "100", "125", "250", "500", "1000", "1250", "2500", "5000",
                                  "12500"]

            if self.hw_type == "PSD/4STD":
                self.steps_min = 0
                self.steps_max = 6000
                self.return_steps_min = 0
                self.return_steps_max = 100
                self.backoff_steps_min = 0
                self.backoff_steps_max = 200

            if self.hw_type == "PSD/4HLF":
                self.steps_min = 0
                self.steps_max = 13714
                self.return_steps_min = 0
                self.return_steps_max = 229
                self.backoff_steps_min = 0
                self.backoff_steps_max = 457

            if self.hw_type == "PSD/4HVT":
                self.steps_min = 0
                self.steps_max = 6000
                self.return_steps_min = 0
                self.return_steps_max = 100
                self.backoff_steps_min = 0
                self.backoff_steps_max = 457

            if self.hw_type == "PSD/4HLF/HVT":
                self.steps_min = 0
                self.steps_max = 13714
                self.return_steps_min = 0
                self.return_steps_max = 229
                self.backoff_steps_min = 0
                self.backoff_steps_max = 229

            if self.hw_type == "PSD/4SF":
                self.steps_min = 0
                self.steps_max = 48000
                self.return_steps_min = 0
                self.return_steps_max = 600
                self.backoff_steps_min = 0
                self.backoff_steps_max = 1600

            if self.hi_res == True:
                self.steps_min *= 8
                self.steps_max *= 8
                self.return_steps_min *= 8
                self.return_steps_max *= 8
                self.backoff_steps_min *= 8
                self.backoff_steps_max *= 8

        if "PSD/6" in self.hw_type:

            self.loop_repeat_min = 0
            self.loop_repeat_max = 65535
            self.delay_min = 5
            self.delay_max = 30000
            self.acceleration_min = 0
            self.acceleration_max = 20
            self.start_velocity_min = 50
            self.start_velocity_max = 800 #empirically 1000 as max was not working but 800 yes (maybe a feature of SmoothFLow stepper?)
            self.syringe_speed_preset_min = 1
            self.syringe_speed_preset_max = 40
            self.stop_velocity_min = 50
            self.stop_velocity_max = 1700 #empirically 2700 as max was not working but 1700 yes (maybe a feature of SmoothFLow stepper?)
            self.syringe_sizes = ["25", "50", "100", "250", "500", "1000", "2500", "5000", "10000", "25000", "50000"]

            if self.hw_type == "PSD/6STD":
                self.max_velocity_min = 2
                self.max_velocity_max = 5800
                self.steps_min = 0
                self.steps_max = 6000
                self.return_steps_min = 0
                self.return_steps_max = 100
                self.backoff_steps_min = 0
                self.backoff_steps_max = 200

            if self.hw_type == "PSD/6HLF":
                self.max_velocity_min = 2
                self.max_velocity_max = 3400
                self.steps_min = 0
                self.steps_max = 13714
                self.return_steps_min = 0
                self.return_steps_max = 229
                self.backoff_steps_min = 0
                self.backoff_steps_max = 457

            if self.hw_type == "PSD/6HVT":
                self.max_velocity_min = 2
                self.max_velocity_max = 5800
                self.steps_min = 0
                self.steps_max = 6000
                self.return_steps_min = 0
                self.return_steps_max = 100
                self.backoff_steps_min = 0
                self.backoff_steps_max = 457

            if self.hw_type == "PSD/6HLF/HVT":
                self.max_velocity_min = 2
                self.max_velocity_max = 3400
                self.steps_min = 0
                self.steps_max = 13714
                self.return_steps_min = 0
                self.return_steps_max = 229
                self.backoff_steps_min = 0
                self.backoff_steps_max = 229

            if self.hw_type == "PSD/6SF":
                self.max_velocity_min = 2
                self.max_velocity_max = 3400
                self.steps_min = 0
                self.steps_max = 48000
                self.return_steps_min = 0
                self.return_steps_max = 600
                self.backoff_steps_min = 0
                self.backoff_steps_max = 1600

            if self.hi_res == True:
                self.steps_min *= 8
                self.steps_max *= 8
                self.return_steps_min *= 8
                self.return_steps_max *= 8
                self.backoff_steps_min *= 8
                self.backoff_steps_max *= 8

    def _send_command(self):
        response = self.com_interface.send_command(self.command_buffer, self.hw_address)
        self.command_buffer = ""
        return response

    def _get_query(self, query_string):
        response = self.com_interface.send_command(query_string, self.hw_address)
        return response

    def run_command(self):
        self.command_buffer += "R"
        return self._send_command()

    def steps_to_volume(self, steps):
        volume = self.syringe_volume / self.steps_max * steps
        return volume

    def volume_to_steps(self, volume):
        steps = volume / self.syringe_volume * self.steps_max
        return steps

    def initialize(self, valve, speed=0):
        if valve == "left":
            self.command_buffer += "Y" + str(speed)
        elif valve == "right":
            self.command_buffer += "Z" + str(speed)
        elif valve == "novalve":
            self.command_buffer += "W" + str(speed)
        else:
            return "No initialization command set."
        return "OK"

    def _general_steps_command(self, command, steps, min, max):
        if steps >= min and steps <= max:
            self.command_buffer += command + str(steps)
            return "OK"
        else:
            return "Steps out of range (%s - %s)" % (min, max)

    def set_step_position(self, steps):
        self._general_steps_command("A", steps, self.steps_min, self.steps_max)

    def reset_syringe_counter_position(self):
        self.command_buffer += "z"
        return "OK"

    def move_down_steps(self, steps):
        self._general_steps_command("P", steps, self.steps_min, self.steps_max)

    def move_up_steps(self, steps):
        self._general_steps_command("D", steps, self.steps_min, self.steps_max)

    def set_return_steps(self, steps):
        self._general_steps_command("K", steps, self.return_steps_min, self.return_steps_max)

    def set_backoff_steps(self, steps):
        self._general_steps_command("k", steps, self.backoff_steps_min, self.backoff_steps_max)

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

    def setHiRes(self):
        self.command_buffer += "N1"
        response = self.run_command()
        self.hi_res = True
        self.load_pump_parameters()
        return response

    def setLoRes(self):
        self.command_buffer += "N0"
        response = self.run_command()
        self.hi_res = False
        self.load_pump_parameters()
        return response

    def set_acceleration(self, acceleration):
        if acceleration >= self.acceleration_min and acceleration <= self.acceleration_max:
            self.command_buffer += "L" + str(acceleration)
            return "OK"
        else:
            return "Acceleration out of range (%s - %s)" % (self.acceleration_min, self.acceleration_max)

    def set_start_velocity(self, start_velocity):
        if start_velocity >= self.start_velocity_min and start_velocity <= self.start_velocity_max:
            self.command_buffer += "v" + str(start_velocity)
            return "OK"
        else:
            return "Start velocity out of range (%s - %s)" % (self.start_velocity_min, self.start_velocity_max)

    def set_max_velocity(self, max_velocity):
        if max_velocity >= self.max_velocity_min and max_velocity <= self.max_velocity_max:
            self.command_buffer += "V" + str(max_velocity)
            return "OK"
        else:
            return "Max velocity out of range (%s - %s)" % (self.max_velocity_min, self.max_velocity_max)

    def set_syringe_speed(self, speed_preset):
        if speed_preset >= self.syringe_speed_preset_min and speed_preset <= self.syringe_speed_preset_max:
            self.command_buffer += "S" + str(speed_preset)
            return "OK"
        else:
            return "Speed preset out of range (%s - %s)" % (
                self.syringe_speed_preset_min, self.syringe_speed_preset_max)

    def set_stop_velocity(self, stop_velocity):
        if stop_velocity >= self.stop_velocity_min and stop_velocity <= self.stop_velocity_max:
            self.command_buffer += "c" + str(stop_velocity)
            return "OK"
        else:
            return "Stop velocity out of range (%s - %s)" % (self.stop_velocity_min, self.stop_velocity_max)

    def terminate(self):
        self.command_buffer += "T"
        self.run_command()
        return "OK"

    def empty_syringe(self, start_velocity=-1, stop_velocity=-1, max_velocity=-1, acceleration=-1):
        # empty the syringe to output port (default max settings)
        self.valve_output()
        self.set_start_velocity(start_velocity) if start_velocity != -1 else self.set_start_velocity(
            self.start_velocity_max)
        self.set_stop_velocity(stop_velocity) if stop_velocity != -1 else self.set_stop_velocity(self.stop_velocity_max)
        self.set_max_velocity(max_velocity) if max_velocity != -1 else self.set_max_velocity(self.max_velocity_max)
        self.set_acceleration(acceleration) if acceleration != -1 else self.set_acceleration(self.acceleration_max)
        self.set_step_position(self.steps_min)

    def fill_syringe(self, start_velocity=-1, stop_velocity=-1, max_velocity=-1, acceleration=-1):
        # fills the syringe from input port (default max settings)
        self.valve_input()
        self.set_start_velocity(start_velocity) if start_velocity != -1 else self.set_start_velocity(
            self.start_velocity_max)
        self.set_stop_velocity(stop_velocity) if stop_velocity != -1 else self.set_stop_velocity(self.stop_velocity_max)
        self.set_max_velocity(max_velocity) if max_velocity != -1 else self.set_max_velocity(self.max_velocity_max)
        self.set_acceleration(acceleration) if acceleration != -1 else self.set_acceleration(self.acceleration_max)
        self.set_step_position(self.steps_max)

    def move_syringe_up(self, valve_port, steps, start_velocity=-1, stop_velocity=-1, max_velocity=-1,
                          acceleration=-1):
        self.valve_input(valve_port)
        self.set_start_velocity(start_velocity) if start_velocity != -1 else self.set_start_velocity(
            self.start_velocity_max)
        self.set_stop_velocity(stop_velocity) if stop_velocity != -1 else self.set_stop_velocity(self.stop_velocity_max)
        self.set_max_velocity(max_velocity) if max_velocity != -1 else self.set_max_velocity(self.max_velocity_max)
        self.set_acceleration(acceleration) if acceleration != -1 else self.set_acceleration(self.acceleration_max)
        self.move_up_steps(steps)

    def move_syringe_down(self, valve_port, steps, start_velocity=-1, stop_velocity=-1, max_velocity=-1, acceleration=-1):
        self.valve_input(valve_port)
        self.set_start_velocity(start_velocity) if start_velocity != -1 else self.set_start_velocity(
            self.start_velocity_max)
        self.set_stop_velocity(stop_velocity) if stop_velocity != -1 else self.set_stop_velocity(self.stop_velocity_max)
        self.set_max_velocity(max_velocity) if max_velocity != -1 else self.set_max_velocity(self.max_velocity_max)
        self.set_acceleration(acceleration) if acceleration != -1 else self.set_acceleration(self.acceleration_max)
        self.move_down_steps(steps)

    def get_command_buffer_status(self):
        return self._get_query("F")

    def get_firmware_version(self):
        return self._get_query("&")

    def get_status(self):
        return self._get_query("Q")

    def get_absolute_syringe_position(self):
        return self._get_query("?")

    def get_start_velocity(self):
        return self._get_query("?1")

    def get_max_velocity(self):
        return self._get_query("?2")

    def get_stop_velocity(self):
        return self._get_query("?3")

    def get_actual_syringe_position(self):
        return self._get_query("?4")

    def get_nr_return_steps(self):
        return self._get_query("?12")

    def get_aux1_status(self):
        return self._get_query("?13")

    def get_aux2_status(self):
        return self._get_query("?14")

    def get_back_off_steps(self):
        return self._get_query("?24")

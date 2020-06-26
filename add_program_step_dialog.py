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

from PyQt5 import QtWidgets

from gui.add_program_step import Ui_DialogAddProgramStep


class DialogAddProgramStep(QtWidgets.QDialog, Ui_DialogAddProgramStep):
    def __init__(self, parent=None, DeviceList=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.Devicelist = DeviceList

        #EVENTS handling
        self.comboBoxDevice.currentTextChanged.connect(self.comboBoxDeviceChanged)
        self.comboBoxBasicCommands.currentTextChanged.connect(self.comboBoxBasicCommandsChanged)
        self.comboBoxComplexCommands.currentTextChanged.connect(self.comboBoxComplexChanged)
        self.comboBoxBasicCommands.activated.connect(self.comboBoxBasicCommandsActivated)
        self.comboBoxComplexCommands.activated.connect(self.comboBoxComplexActivated)
        self.spinBoxSteps.valueChanged.connect(self.spinBoxStepsValueChanged)
        self.spinBoxVolume.valueChanged.connect(self.spinBoxVolumeValueChanged)
        self.spinBoxSpeedSteps.valueChanged.connect(self.spinBoxSpeedStepsValueChanged)
        self.spinBoxSpeedVolume.valueChanged.connect(self.spinBoxSpeedVolumeValueChanged)

    def spinBoxStepsValueChanged(self, value):
        if self.spinBoxSteps.hasFocus():
            currentIndex = self.comboBoxDevice.currentIndex()
            self.spinBoxVolume.setValue(self.Devicelist[currentIndex].steps_to_volume(value))

    def spinBoxVolumeValueChanged(self, value):
        if self.spinBoxVolume.hasFocus():
            currentIndex = self.comboBoxDevice.currentIndex()
            self.spinBoxSteps.setValue(int(self.Devicelist[currentIndex].volume_to_steps(value)))

    def spinBoxSpeedStepsValueChanged(self, value):
        if self.spinBoxSpeedSteps.hasFocus():
            currentIndex = self.comboBoxDevice.currentIndex()
            self.spinBoxSpeedVolume.setValue(self.Devicelist[currentIndex].steps_to_volume(value))

    def spinBoxSpeedVolumeValueChanged(self, value):
        if self.spinBoxSpeedVolume.hasFocus():
            currentIndex = self.comboBoxDevice.currentIndex()
            self.spinBoxSpeedSteps.setValue(int(self.Devicelist[currentIndex].volume_to_steps(value)))

    def comboBoxDeviceChanged(self, value):
        if "PSD" in value:
            self.comboBoxBasicCommands.enabled = True
            self.comboBoxBasicCommands.clear()
            self.comboBoxBasicCommands.addItems([
                "initialize",
                "set_step_position",
                "move_up_steps",
                "move_down_steps",
                "set_return_steps",
                "set_backoff_steps",
                "valve_input",
                "valve_output",
                "valve_bypass",
                "valve_extra",
                "insert_loop_start",
                "insert_loop_end",
                "delay",
                "halt",
                "setHiRes",
                "setLoRes",
                "set_acceleration",
                "set_start_velocity",
                "set_max_velocity",
                "set_syringe_speed",
                "set_stop_velocity"
            ])
            self.comboBoxBasicCommands.setCurrentIndex(-1)
            self.comboBoxComplexCommands.enabled = True
            self.comboBoxComplexCommands.clear()
            self.comboBoxComplexCommands.addItems([
                "empty_syringe",
                "fill_syringe",
                "move_syringe_up",
                "move_syringe_down"])
            self.comboBoxComplexCommands.setCurrentIndex(-1)
        if "MVP" in value:
            self.comboBoxBasicCommands.enabled = True
            self.comboBoxBasicCommands.clear()
            self.comboBoxBasicCommands.addItems([
                "initialize",
                "valve_input",
                "valve_output",
                "valve_bypass",
                "valve_extra",
                "insert_loop_start",
                "insert_loop_end",
                "delay",
                "halt"])
            self.comboBoxComplexCommands.enabled = False
            self.comboBoxComplexCommands.clear()

        self.groupBoxValve.setEnabled(False)
        self.groupBoxSetSteps.setEnabled(False)
        self.groupBoxPumpSpeed.setEnabled(False)

        self.textEditDescription.clear()

    def comboBoxBasicCommandsActivated(self):
        self.comboBoxComplexCommands.setCurrentIndex(-1)

    def comboBoxBasicCommandsChanged(self, value):
        currentIndex = self.comboBoxDevice.currentIndex()
        if value != "":
            self.textEditDescription.clear()
            self.textEditDescription.append(self.Devicelist[currentIndex].command_description[value])
        if value == "initialize":
            self.groupBoxValve.setEnabled(True)
            self.groupBoxPumpSpeed.setDisabled(True)
            self.groupBoxSetSteps.setDisabled(True)
            self.radioButtonOutputLeft.setEnabled(True)
            self.radioButtonOutputRight.setEnabled(True)
            self.labelValvePort.setEnabled(False)
            self.spinBoxValvePort.setEnabled(False)
        elif value in ["set_step_position", "move_up_steps", "move_down_steps", "set_return_steps", "set_backoff_steps",
                       "insert_loop_start"]:
            self.groupBoxValve.setDisabled(True)
            self.groupBoxPumpSpeed.setDisabled(True)
            self.groupBoxSetSteps.setEnabled(True)
            self.spinBoxVolume.setEnabled(True)

            if value in ["set_step_position", "move_up_steps", "move_down_steps"]:
                self.spinBoxSteps.setMinimum(self.Devicelist[currentIndex].steps_min)
                self.spinBoxSteps.setMaximum(self.Devicelist[currentIndex].steps_max)
                self.spinBoxVolume.setMinimum(
                    self.Devicelist[currentIndex].steps_to_volume(self.Devicelist[currentIndex].steps_min))
                self.spinBoxVolume.setMaximum(
                    self.Devicelist[currentIndex].steps_to_volume(self.Devicelist[currentIndex].steps_max))

            if value == "set_return_steps":
                self.spinBoxSteps.setMinimum(self.Devicelist[currentIndex].return_steps_min)
                self.spinBoxSteps.setMaximum(self.Devicelist[currentIndex].return_steps_max)
                self.spinBoxVolume.setMinimum(
                    self.Devicelist[currentIndex].steps_to_volume(self.Devicelist[currentIndex].return_steps_min))
                self.spinBoxVolume.setMaximum(
                    self.Devicelist[currentIndex].steps_to_volume(self.Devicelist[currentIndex].return_steps_max))

            if value == "set_backoff_steps":
                self.spinBoxSteps.setMinimum(self.Devicelist[currentIndex].backoff_steps_min)
                self.spinBoxSteps.setMaximum(self.Devicelist[currentIndex].backoff_steps_max)
                self.spinBoxVolume.setMinimum(
                    self.Devicelist[currentIndex].steps_to_volume(self.Devicelist[currentIndex].backoff_steps_min))
                self.spinBoxVolume.setMaximum(
                    self.Devicelist[currentIndex].steps_to_volume(self.Devicelist[currentIndex].backoff_steps_max))

            if value == "insert_loop_start":
                self.spinBoxSteps.setMinimum(1)
                self.spinBoxSteps.setMaximum(1000)
                self.spinBoxVolume.setEnabled(False)

            self.spinBoxSteps.setToolTip(str(self.spinBoxSteps.minimum()) + "-" + str(self.spinBoxSteps.maximum()))
            self.spinBoxVolume.setToolTip(str(self.spinBoxVolume.minimum()) + "-" + str(self.spinBoxVolume.maximum()))

        elif value in ["valve_input", "valve_output"]:
            self.groupBoxValve.setEnabled(True)
            self.groupBoxPumpSpeed.setDisabled(True)
            self.groupBoxSetSteps.setDisabled(True)
            self.radioButtonOutputLeft.setEnabled(False)
            self.radioButtonOutputRight.setEnabled(False)
            self.labelValvePort.setEnabled(True)
            self.spinBoxValvePort.setEnabled(True)

        elif value in ["valve_bypass", "valve_extra"]:
            self.groupBoxValve.setEnabled(False)
            self.groupBoxPumpSpeed.setDisabled(True)
            self.groupBoxSetSteps.setDisabled(True)
            self.radioButtonOutputLeft.setEnabled(False)
            self.radioButtonOutputRight.setEnabled(False)
            self.labelValvePort.setEnabled(False)
            self.spinBoxValvePort.setEnabled(False)

        elif value in ["insert_loop_end", "halt", "setHiRes", "setLoRes"]:
            self.groupBoxValve.setDisabled(True)
            self.groupBoxPumpSpeed.setDisabled(True)
            self.groupBoxSetSteps.setDisabled(True)
        elif value in ["set_acceleration", "set_start_velocity", "set_max_velocity", "set_syringe_speed",
                       "set_stop_velocity"]:
            self.groupBoxValve.setDisabled(True)
            self.groupBoxPumpSpeed.setEnabled(True)
            self.groupBoxSetSteps.setDisabled(True)
            if value == "set_acceleration":
                self.labelAcceleration.setEnabled(True)
                self.spinBoxAcceleration.setEnabled(True)
                self.labelSpeedSteps.setEnabled(False)
                self.spinBoxSpeedSteps.setEnabled(False)
                self.labelSpeedSyringe.setEnabled(False)
                self.spinBoxSpeedSyringe.setEnabled(False)
                self.labelSpeedVolume.setEnabled(False)
                self.spinBoxSpeedVolume.setEnabled(False)
                self.labelStartVelocity.setEnabled(False)
                self.spinBoxStartVelocity.setEnabled(False)
                self.labelStopVelocity.setEnabled(False)
                self.spinBoxStopVelocity.setEnabled(False)
                self.spinBoxAcceleration.setMinimum(self.Devicelist[currentIndex].acceleration_min)
                self.spinBoxAcceleration.setMaximum(self.Devicelist[currentIndex].acceleration_max)
                self.spinBoxAcceleration.setToolTip(
                    str(self.spinBoxAcceleration.minimum()) + "-" + str(self.spinBoxAcceleration.maximum()))

            elif value == "set_start_velocity":
                self.labelAcceleration.setEnabled(False)
                self.spinBoxAcceleration.setEnabled(False)
                self.labelSpeedSteps.setEnabled(False)
                self.spinBoxSpeedSteps.setEnabled(False)
                self.labelSpeedSyringe.setEnabled(False)
                self.spinBoxSpeedSyringe.setEnabled(False)
                self.labelSpeedVolume.setEnabled(False)
                self.spinBoxSpeedVolume.setEnabled(False)
                self.labelStartVelocity.setEnabled(True)
                self.spinBoxStartVelocity.setEnabled(True)
                self.labelStopVelocity.setEnabled(False)
                self.spinBoxStopVelocity.setEnabled(False)
                self.spinBoxStartVelocity.setMinimum(self.Devicelist[currentIndex].start_velocity_min)
                self.spinBoxStartVelocity.setMaximum(self.Devicelist[currentIndex].start_velocity_max)
                self.spinBoxStartVelocity.setToolTip(
                    str(self.spinBoxStartVelocity.minimum()) + "-" + str(self.spinBoxStartVelocity.maximum()))
            elif value == "set_stop_velocity":
                self.labelAcceleration.setEnabled(False)
                self.spinBoxAcceleration.setEnabled(False)
                self.labelSpeedSteps.setEnabled(False)
                self.spinBoxSpeedSteps.setEnabled(False)
                self.labelSpeedSyringe.setEnabled(False)
                self.spinBoxSpeedSyringe.setEnabled(False)
                self.labelSpeedVolume.setEnabled(False)
                self.spinBoxSpeedVolume.setEnabled(False)
                self.labelStartVelocity.setEnabled(False)
                self.spinBoxStartVelocity.setEnabled(False)
                self.labelStopVelocity.setEnabled(True)
                self.spinBoxStopVelocity.setEnabled(True)
                self.spinBoxStopVelocity.setMinimum(self.Devicelist[currentIndex].stop_velocity_min)
                self.spinBoxStopVelocity.setMaximum(self.Devicelist[currentIndex].stop_velocity_max)
                self.spinBoxStopVelocity.setToolTip(
                    str(self.spinBoxStopVelocity.minimum()) + "-" + str(self.spinBoxStopVelocity.maximum()))
            elif value == "set_max_velocity":
                self.labelAcceleration.setEnabled(False)
                self.spinBoxAcceleration.setEnabled(False)
                self.labelSpeedSteps.setEnabled(True)
                self.spinBoxSpeedSteps.setEnabled(True)
                self.labelSpeedVolume.setEnabled(True)
                self.spinBoxSpeedVolume.setEnabled(True)
                self.labelSpeedSyringe.setEnabled(False)
                self.spinBoxSpeedSyringe.setEnabled(False)
                self.labelStartVelocity.setEnabled(False)
                self.spinBoxStartVelocity.setEnabled(False)
                self.labelStopVelocity.setEnabled(False)
                self.spinBoxStopVelocity.setEnabled(False)
                self.spinBoxSpeedSteps.setMinimum(self.Devicelist[currentIndex].max_velocity_min)
                self.spinBoxSpeedSteps.setMaximum(self.Devicelist[currentIndex].max_velocity_max)
                self.spinBoxSpeedVolume.setMinimum(
                    self.spinBoxSpeedSteps.minimum() * self.Devicelist[currentIndex].syringe_volume / self.Devicelist[
                        currentIndex].steps_max)
                self.spinBoxSpeedVolume.setMaximum(
                    self.spinBoxSpeedSteps.maximum() * self.Devicelist[currentIndex].syringe_volume / self.Devicelist[
                        currentIndex].steps_max)

                self.spinBoxSpeedSteps.setToolTip(
                    str(self.spinBoxSpeedSteps.minimum()) + "-" + str(self.spinBoxSpeedSteps.maximum()))
                self.spinBoxSpeedVolume.setToolTip(
                    str(self.spinBoxSpeedVolume.minimum()) + "-" + str(self.spinBoxSpeedVolume.maximum()))

            elif value == "set_syringe_speed":
                self.labelAcceleration.setEnabled(False)
                self.spinBoxAcceleration.setEnabled(False)
                self.labelSpeedSteps.setEnabled(False)
                self.spinBoxSpeedSteps.setEnabled(False)
                self.labelSpeedSyringe.setEnabled(True)
                self.spinBoxSpeedSyringe.setEnabled(True)
                self.labelSpeedVolume.setEnabled(False)
                self.spinBoxSpeedVolume.setEnabled(False)
                self.labelStartVelocity.setEnabled(False)
                self.spinBoxStartVelocity.setEnabled(False)
                self.labelStopVelocity.setEnabled(False)
                self.spinBoxStopVelocity.setEnabled(False)
                self.spinBoxSpeedSyringe.setMinimum(self.Devicelist[currentIndex].syringe_speed_preset_min)
                self.spinBoxSpeedSyringe.setMaximum(self.Devicelist[currentIndex].syringe_speed_preset_max)
                self.spinBoxSpeedSyringe.setToolTip(
                    str(self.spinBoxSpeedSyringe.minimum()) + "-" + str(self.spinBoxSpeedSyringe.maximum()))

    def comboBoxComplexActivated(self):
        self.comboBoxBasicCommands.setCurrentIndex(-1)

    def comboBoxComplexChanged(self, value):
        currentIndex = self.comboBoxDevice.currentIndex()
        if value != "":
            self.textEditDescription.clear()
            self.textEditDescription.append(self.Devicelist[currentIndex].command_description[value])
        if value in ["empty_syringe", "fill_syringe"]:
            self.groupBoxValve.setDisabled(True)
            self.groupBoxPumpSpeed.setEnabled(True)
            self.groupBoxSetSteps.setEnabled(False)
            self.labelAcceleration.setEnabled(True)
            self.spinBoxAcceleration.setEnabled(True)
            self.labelSpeedSteps.setEnabled(True)
            self.spinBoxSpeedSteps.setEnabled(True)
            self.labelSpeedVolume.setEnabled(True)
            self.spinBoxSpeedVolume.setEnabled(True)
            self.labelStartVelocity.setEnabled(True)
            self.spinBoxStartVelocity.setEnabled(True)
            self.labelStopVelocity.setEnabled(True)
            self.spinBoxStopVelocity.setEnabled(True)
            self.labelSpeedSyringe.setEnabled(False)
            self.spinBoxSpeedSyringe.setEnabled(False)
            self.spinBoxAcceleration.setMinimum(self.Devicelist[currentIndex].acceleration_min)
            self.spinBoxAcceleration.setMaximum(self.Devicelist[currentIndex].acceleration_max)
            self.spinBoxAcceleration.setToolTip(
                str(self.spinBoxAcceleration.minimum()) + "-" + str(self.spinBoxAcceleration.maximum()))
            self.spinBoxStartVelocity.setMinimum(self.Devicelist[currentIndex].start_velocity_min)
            self.spinBoxStartVelocity.setMaximum(self.Devicelist[currentIndex].start_velocity_max)
            self.spinBoxStartVelocity.setToolTip(
                str(self.spinBoxStartVelocity.minimum()) + "-" + str(self.spinBoxStartVelocity.maximum()))
            self.spinBoxStopVelocity.setMinimum(self.Devicelist[currentIndex].stop_velocity_min)
            self.spinBoxStopVelocity.setMaximum(self.Devicelist[currentIndex].stop_velocity_max)
            self.spinBoxStopVelocity.setToolTip(
                str(self.spinBoxStopVelocity.minimum()) + "-" + str(self.spinBoxStopVelocity.maximum()))
            self.spinBoxSpeedSteps.setMinimum(self.Devicelist[currentIndex].max_velocity_min)
            self.spinBoxSpeedSteps.setMaximum(self.Devicelist[currentIndex].max_velocity_max)
            self.spinBoxSpeedVolume.setMinimum(
                self.spinBoxSpeedSteps.minimum() * self.Devicelist[currentIndex].syringe_volume / self.Devicelist[
                    currentIndex].steps_max)
            self.spinBoxSpeedVolume.setMaximum(
                self.spinBoxSpeedSteps.maximum() * self.Devicelist[currentIndex].syringe_volume / self.Devicelist[
                    currentIndex].steps_max)

            self.spinBoxSpeedSteps.setToolTip(
                str(self.spinBoxSpeedSteps.minimum()) + "-" + str(self.spinBoxSpeedSteps.maximum()))
            self.spinBoxSpeedVolume.setToolTip(
                str(self.spinBoxSpeedVolume.minimum()) + "-" + str(self.spinBoxSpeedVolume.maximum()))

        if value in ["move_syringe_up", "move_syringe_down"]:
            self.groupBoxValve.setEnabled(True)
            self.groupBoxPumpSpeed.setEnabled(True)
            self.groupBoxSetSteps.setEnabled(True)
            self.labelAcceleration.setEnabled(True)
            self.spinBoxAcceleration.setEnabled(True)
            self.labelSpeedSteps.setEnabled(True)
            self.spinBoxSpeedSteps.setEnabled(True)
            self.labelSpeedVolume.setEnabled(True)
            self.spinBoxSpeedVolume.setEnabled(True)
            self.labelStartVelocity.setEnabled(True)
            self.spinBoxStartVelocity.setEnabled(True)
            self.labelStopVelocity.setEnabled(True)
            self.spinBoxStopVelocity.setEnabled(True)
            self.labelSpeedSyringe.setEnabled(False)
            self.spinBoxSpeedSyringe.setEnabled(False)
            self.radioButtonOutputLeft.setEnabled(False)
            self.radioButtonOutputRight.setEnabled(False)
            self.labelValvePort.setEnabled(True)
            self.spinBoxValvePort.setEnabled(True)
            self.spinBoxSteps.setMinimum(self.Devicelist[currentIndex].steps_min)
            self.spinBoxSteps.setMaximum(self.Devicelist[currentIndex].steps_max)
            self.spinBoxVolume.setMinimum(
                self.spinBoxSteps.minimum() * self.Devicelist[currentIndex].syringe_volume / self.Devicelist[
                    currentIndex].steps_max)
            self.spinBoxVolume.setMaximum(
                self.spinBoxSteps.maximum() * self.Devicelist[currentIndex].syringe_volume / self.Devicelist[
                    currentIndex].steps_max)
            self.spinBoxAcceleration.setMinimum(self.Devicelist[currentIndex].acceleration_min)
            self.spinBoxAcceleration.setMaximum(self.Devicelist[currentIndex].acceleration_max)
            self.spinBoxAcceleration.setToolTip(
                str(self.spinBoxAcceleration.minimum()) + "-" + str(self.spinBoxAcceleration.maximum()))
            self.spinBoxStartVelocity.setMinimum(self.Devicelist[currentIndex].start_velocity_min)
            self.spinBoxStartVelocity.setMaximum(self.Devicelist[currentIndex].start_velocity_max)
            self.spinBoxStartVelocity.setToolTip(
                str(self.spinBoxStartVelocity.minimum()) + "-" + str(self.spinBoxStartVelocity.maximum()))
            self.spinBoxStopVelocity.setMinimum(self.Devicelist[currentIndex].stop_velocity_min)
            self.spinBoxStopVelocity.setMaximum(self.Devicelist[currentIndex].stop_velocity_max)
            self.spinBoxStopVelocity.setToolTip(
                str(self.spinBoxStopVelocity.minimum()) + "-" + str(self.spinBoxStopVelocity.maximum()))
            self.spinBoxSpeedSteps.setMinimum(self.Devicelist[currentIndex].max_velocity_min)
            self.spinBoxSpeedSteps.setMaximum(self.Devicelist[currentIndex].max_velocity_max)
            self.spinBoxSpeedVolume.setMinimum(
                self.spinBoxSpeedSteps.minimum() * self.Devicelist[currentIndex].syringe_volume / self.Devicelist[
                    currentIndex].steps_max)
            self.spinBoxSpeedVolume.setMaximum(
                self.spinBoxSpeedSteps.maximum() * self.Devicelist[currentIndex].syringe_volume / self.Devicelist[
                    currentIndex].steps_max)

            self.spinBoxSpeedSteps.setToolTip(
                str(self.spinBoxSpeedSteps.minimum()) + "-" + str(self.spinBoxSpeedSteps.maximum()))
            self.spinBoxSpeedVolume.setToolTip(
                str(self.spinBoxSpeedVolume.minimum()) + "-" + str(self.spinBoxSpeedVolume.maximum()))

    def showEvent(self, event):
        id = 1

        for device in self.Devicelist:
            self.comboBoxDevice.addItem(str(id) + " - " + device.hw_type)
            id += 1
        self.comboBoxDevice.setCurrentIndex(-1)
        self.comboBoxBasicCommands.setCurrentIndex(-1)
        self.comboBoxBasicCommands.clear()
        self.comboBoxComplexCommands.setCurrentIndex(-1)
        self.comboBoxComplexCommands.clear()

        self.textEditDescription.clear()
        event.accept()

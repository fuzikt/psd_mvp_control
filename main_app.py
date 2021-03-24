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
# Main GUI PSD/MVP controlling application
# **************************************************************************

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

from gui.main_window import Ui_MainWindow
from add_devices_dialog import DialogAddDevice
from add_program_step_dialog import DialogAddProgramStep
from com_log_dialog import DialogComLog

from hw_classes.psd_pump import PSDpump
from hw_classes.mvp_valve import MVPvalve

import serial.tools.list_ports


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # EVENTS
        self.buttonDeviceAdd.clicked.connect(self.clickButtonDeviceAdd)
        self.buttonProgramStepInsert.clicked.connect(self.clickButtonInsertProgramStep)
        self.buttonProgramStepEdit.clicked.connect(self.clickButtonEditProgramStep)
        self.buttonRunSingleCommand.clicked.connect(self.clickButtonRunSingleCommand)
        self.buttonRun.clicked.connect(self.clickButtonRun)
        self.buttonStop.clicked.connect(self.clickButtonStop)
        self.buttonProgramStepRemove.clicked.connect(self.clickButtonProgramStepRemove)
        self.buttonDeviceRemove.clicked.connect(self.clickButtonDevicesRemove)
        self.buttonSave.clicked.connect(self.clickButtonSave)
        self.buttonOpen.clicked.connect(self.clickButtonOpen)
        self.buttonComLog.clicked.connect(self.clickButtonCOMLog)

        # tableDevices setup
        self.tableDevices.setColumnCount(5)
        self.tableDevices.setHorizontalHeaderLabels(['Device', 'HW address', 'COM port', 'Syringe', 'Hi res'])
        self.tableDevices.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        QtWidgets.QTableWidget.resizeRowsToContents(self.tableDevices)
        QtWidgets.QTableWidget.resizeColumnsToContents(self.tableDevices)
        self.tableDevices.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableDevices.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # tableProgram setup
        self.tableProgram.setColumnCount(3)
        self.tableProgram.setHorizontalHeaderLabels(['Device', 'Command', 'Parameters'])
        self.tableProgram.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        QtWidgets.QTableWidget.resizeRowsToContents(self.tableProgram)
        QtWidgets.QTableWidget.resizeColumnsToContents(self.tableProgram)
        self.tableProgram.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableProgram.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # object local variables
        self.deviceList = []  # defined as [device_type, hw_address, com_port, hi_res, syringe_type]
        self.programSteps = []  # defined as [device_id, command, [param1, param2]]
        self.deviceInCharge = 0  # device from deviceList actually running a command
        self.devicesReady = True  # readiness of the last device that run a command
        self.currentProgramStepExecuted = 0
        self.terminateProgram = False  # whether Stop button was pressed
        self.loopStartStep = 0
        self.loopMaxRepeat = 0
        self.loopCurrentRepeat = 0

        # timers for background processing with their timeout events
        self.getStateTimer = QtCore.QTimer()
        self.getStateTimer.timeout.connect(self.getStateTimerTimeOut)

        self.runTimer = QtCore.QTimer()
        self.runTimer.timeout.connect(self.runTimerTimeOut)

        self.DialogComWindow = DialogComLog()
        self.debug_communication = self.DialogComWindow.isVisible

    def clickButtonCOMLog(self):
        self.DialogComWindow.show()

    def clickButtonRunSingleCommand(self):
        if self.tableProgram.currentRow() == -1:
            return
        # start and end loop are non-runnable steps
        if self.programSteps[self.tableProgram.currentRow()][1] == "insert_loop_start" or \
                self.programSteps[self.tableProgram.currentRow()][1] == "insert_loop_end":
            return
        self.labelInfo.setText("Busy...")
        self.disableButtons()
        self.deviceInCharge = self.programSteps[self.tableProgram.currentRow()][0]
        self.runSingleCommand(self.programSteps[self.tableProgram.currentRow()][0],
                              self.programSteps[self.tableProgram.currentRow()][1],
                              self.programSteps[self.tableProgram.currentRow()][2])
        # wait until device becomes available
        self.getStateTimer.start(100)

    def clickButtonStop(self):
        for deviceID in range(len(self.deviceList)):
            self.deviceList[deviceID].terminate()
            self.terminateProgram = True

    def clickButtonRun(self):
        self.terminateProgram = False
        self.currentProgramStepExecuted = 0
        if self.programSteps[self.currentProgramStepExecuted][1] == "insert_loop_start":
            self.loopStartStep = self.currentProgramStepExecuted
            self.loopMaxRepeat = self.programSteps[self.currentProgramStepExecuted][2][0]
            self.loopCurrentRepeat = 1
            self.labelRepeatStatus.setText(str(self.loopCurrentRepeat) + "/" + str(self.loopMaxRepeat))
            self.currentProgramStepExecuted += 1

        self.tableProgram.setCurrentCell(self.currentProgramStepExecuted, 0)
        self.labelInfo.setText("Busy...")
        self.disableButtons()
        self.deviceInCharge = self.programSteps[self.currentProgramStepExecuted][0]
        self.runSingleCommand(self.programSteps[self.currentProgramStepExecuted][0],
                              self.programSteps[self.currentProgramStepExecuted][1],
                              self.programSteps[self.currentProgramStepExecuted][2])

        self.runTimer.start(100)

    def runTimerTimeOut(self):
        if self.queryDeviceForReadiness(self.deviceInCharge):
            if self.currentProgramStepExecuted + 1 <= len(self.programSteps) - 1 and not self.terminateProgram:
                self.currentProgramStepExecuted += 1
                if self.programSteps[self.currentProgramStepExecuted][1] == "insert_loop_start":
                    self.loopStartStep = self.currentProgramStepExecuted
                    self.loopMaxRepeat = self.programSteps[self.currentProgramStepExecuted][2][0]
                    self.loopCurrentRepeat = 1
                    self.labelRepeatStatus.setText(str(self.loopCurrentRepeat) + "/" + str(self.loopMaxRepeat))
                else:
                    if self.programSteps[self.currentProgramStepExecuted][
                        1] == "insert_loop_end" and self.loopCurrentRepeat < self.loopMaxRepeat:
                        self.currentProgramStepExecuted = self.loopStartStep + 1
                        self.loopCurrentRepeat += 1
                        self.labelRepeatStatus.setText(str(self.loopCurrentRepeat) + "/" + str(self.loopMaxRepeat))
                    elif self.programSteps[self.currentProgramStepExecuted][
                        1] == "insert_loop_end" and self.loopCurrentRepeat >= self.loopMaxRepeat:
                        self.labelRepeatStatus.setText("-/-")
                        if self.currentProgramStepExecuted + 1 < len(self.programSteps) - 1:
                            self.currentProgramStepExecuted += 1
                        else:
                            return
                    self.tableProgram.setCurrentCell(self.currentProgramStepExecuted, 0)
                    self.labelInfo.setText("Busy...")
                    self.disableButtons()
                    self.deviceInCharge = self.programSteps[self.currentProgramStepExecuted][0]
                    self.runSingleCommand(self.programSteps[self.currentProgramStepExecuted][0],
                                          self.programSteps[self.currentProgramStepExecuted][1],
                                          self.programSteps[self.currentProgramStepExecuted][2])
            else:
                self.devicesReady = True
                self.labelInfo.setText("Ready")
                self.enableButtons()
                self.loopStartStep = 0
                self.loopMaxRepeat = 0
                self.loopCurrentRepeat = 0
                self.terminateProgram = False
                self.runTimer.stop()
        else:
            self.devicesReady = False
            self.labelInfo.setText("Busy...")
            self.disableButtons()
            return

    def getStateTimerTimeOut(self):
        if self.queryDeviceForReadiness(self.deviceInCharge):
            self.devicesReady = True
            self.labelInfo.setText("Ready")
            self.enableButtons()
            self.getStateTimer.stop()
        else:
            self.devicesReady = False
            self.labelInfo.setText("Busy...")
            self.disableButtons()
            return

    def runSingleCommand(self, device, command, params):
        method_to_call = getattr(self.deviceList[device], command)
        result = method_to_call(*params)

        if self.debug_communication():
            self.DialogComWindow.comunicationLogList.addItem(
                QtWidgets.QListWidgetItem("DEV%s COMMAND: %sR" % (device + 1, self.deviceList[device].command_buffer)))

        response = self.deviceList[device].run_command()

        if self.debug_communication():
            self.DialogComWindow.comunicationLogList.addItem(
                QtWidgets.QListWidgetItem("DEV%s RESPONSE: %s" % (device + 1, str(response))))

    def queryDeviceForReadiness(self, device):
        if self.debug_communication():
            self.DialogComWindow.comunicationLogList.addItem(QtWidgets.QListWidgetItem("DEV%s COMMAND: Q" % (device + 1)))

        readiness = self.deviceList[device].get_status()

        if self.debug_communication():
            self.DialogComWindow.comunicationLogList.addItem(
                QtWidgets.QListWidgetItem(("DEV%s RESPONSE: %s" % (device + 1, str(readiness)))))

        if readiness[1]:
            return True
        else:
            return False

    def disableButtons(self):
        self.buttonRun.setEnabled(False)
        self.buttonRunSingleCommand.setEnabled(False)
        self.buttonDeviceAdd.setEnabled(False)
        self.buttonDeviceRemove.setEnabled(False)
        self.buttonProgramStepInsert.setEnabled(False)
        self.buttonProgramStepEdit.setEnabled(False)
        self.buttonProgramStepRemove.setEnabled(False)
        self.tableProgram.setEnabled(False)
        self.tableDevices.setEnabled(False)
        # ENABLE STOP BUTTON
        self.buttonStop.setEnabled(True)

    def enableButtons(self):
        self.buttonRun.setEnabled(True)
        self.buttonRunSingleCommand.setEnabled(True)
        self.buttonDeviceAdd.setEnabled(True)
        self.buttonDeviceRemove.setEnabled(True)
        self.buttonProgramStepInsert.setEnabled(True)
        self.buttonProgramStepEdit.setEnabled(True)
        self.buttonProgramStepRemove.setEnabled(True)
        self.tableProgram.setEnabled(True)
        self.tableDevices.setEnabled(True)
        # DISABLE STOP BUTTON
        self.buttonStop.setEnabled(False)

    def addEditProgramStep(self, addEditDialog, Editing):

        programCommand = addEditDialog.comboBoxBasicCommands.currentText() + addEditDialog.comboBoxComplexCommands.currentText()
        deviceID = addEditDialog.comboBoxDevice.currentIndex()
        commandParameters = []

        if programCommand == "":
            return

        if programCommand == "initialize":
            if addEditDialog.radioButtonOutputRight.isChecked():
                commandParameters.append("right")
            else:
                commandParameters.append("left")

        elif programCommand in ["set_step_position", "move_up_steps", "move_down_steps", "set_return_steps",
                                "set_backoff_steps"]:
            commandParameters.append(addEditDialog.spinBoxSteps.value())

        elif programCommand in ["valve_input", "valve_output"]:
            commandParameters.append(addEditDialog.spinBoxValvePort.value())

        elif programCommand in ["valve_bypass", "valve_extra", "halt", "setHiRes", "setLoRes", "insert_loop_end"]:
            pass

        elif programCommand in ["insert_loop_start"]:
            commandParameters.append(addEditDialog.spinBoxSteps.value())

        elif programCommand == "set_acceleration":
            commandParameters.append(addEditDialog.spinBoxAcceleration.value())

        elif programCommand == "set_start_velocity":
            commandParameters.append(addEditDialog.spinBoxStartVelocity.value())

        elif programCommand == "set_stop_velocity":
            commandParameters.append(addEditDialog.spinBoxStopVelocity.value())

        elif programCommand == "set_max_velocity":
            commandParameters.append(addEditDialog.spinBoxSpeedSteps.value())

        elif programCommand == "set_syringe_speed":
            commandParameters.append(addEditDialog.spinBoxSpeedSyringe.value())

        elif programCommand in ["empty_syringe", "fill_syringe"]:
            commandParameters.append(addEditDialog.spinBoxStartVelocity.value())
            commandParameters.append(addEditDialog.spinBoxStopVelocity.value())
            commandParameters.append(addEditDialog.spinBoxSpeedSteps.value())
            commandParameters.append(addEditDialog.spinBoxAcceleration.value())

        elif programCommand in ["move_syringe_up", "move_syringe_down"]:
            commandParameters.append(addEditDialog.spinBoxValvePort.value())
            commandParameters.append(addEditDialog.spinBoxSteps.value())
            commandParameters.append(addEditDialog.spinBoxStartVelocity.value())
            commandParameters.append(addEditDialog.spinBoxStopVelocity.value())
            commandParameters.append(addEditDialog.spinBoxSpeedSteps.value())
            commandParameters.append(addEditDialog.spinBoxAcceleration.value())

        if Editing == True:
            self.programSteps[self.tableProgram.currentRow()] = [deviceID, programCommand, commandParameters]
            self.programTableInsertEditRow(self.tableProgram.currentRow(), Editing=True)
            self.tableProgram.setCurrentCell(self.tableProgram.currentRow() + 1, 0)
        else:
            self.programSteps.insert(self.tableProgram.currentRow() + 1, [deviceID, programCommand, commandParameters])
            self.programTableInsertEditRow(self.tableProgram.currentRow() + 1)
            self.tableProgram.setCurrentCell(self.tableProgram.currentRow() + 1, 0)

    def clickButtonInsertProgramStep(self):
        d1 = DialogAddProgramStep(self, DeviceList=self.deviceList)
        d1.show()
        result = d1.exec()
        if result:
            self.addEditProgramStep(d1, False)

    def clickButtonEditProgramStep(self):

        stepToEdit = self.tableProgram.currentRow()
        if stepToEdit == -1:
            QtWidgets.QMessageBox.critical(self, 'Error', "Please, select a program step form the list.",
                                           QMessageBox.Ok)
            return

        programStepToEdit = self.programSteps[stepToEdit]

        d1 = DialogAddProgramStep(self, DeviceList=self.deviceList, Editing=True, ProgramStepToEdit=programStepToEdit)
        d1.show()
        result = d1.exec()
        if result:
            self.addEditProgramStep(d1, True)

    def programTableInsertEditRow(self, programListIndex, Editing=False):

        programCommand = self.programSteps[programListIndex][1]
        tableCommandParameters = []

        if programCommand == "":
            return

        if programCommand == "initialize":
            tableCommandParameters.append("Output valve: %s" % self.programSteps[programListIndex][2][0])

        elif programCommand in ["set_step_position", "move_up_steps", "move_down_steps", "set_return_steps",
                                "set_backoff_steps"]:
            tableCommandParameters.append("Steps: %s" % self.programSteps[programListIndex][2][0])
            tableCommandParameters.append(
                "Volume [ul]: %.2f" % self.deviceList[self.programSteps[programListIndex][0]].steps_to_volume(
                    self.programSteps[programListIndex][2][0]))

        elif programCommand in ["valve_input", "valve_output"]:
            tableCommandParameters.append("Port: %s" % self.programSteps[programListIndex][2][0])

        elif programCommand in ["valve_bypass", "valve_extra", "halt", "setHiRes", "setLoRes", "insert_loop_end"]:
            pass

        elif programCommand in ["insert_loop_start"]:
            tableCommandParameters.append("Repeat: %s x" % self.programSteps[programListIndex][2][0])

        elif programCommand == "set_acceleration":
            tableCommandParameters.append("Acceleration: %s" % self.programSteps[programListIndex][2][0])

        elif programCommand == "set_start_velocity":
            tableCommandParameters.append("Start velocity: %s" % self.programSteps[programListIndex][2][0])

        elif programCommand == "set_stop_velocity":
            tableCommandParameters.append("Stop velocity: %s" % self.programSteps[programListIndex][2][0])

        elif programCommand == "set_max_velocity":
            tableCommandParameters.append("Speed [steps/s]: %s" % self.programSteps[programListIndex][2][0])
            tableCommandParameters.append(
                "Volume [ul/s]: %.2f" % self.deviceList[self.programSteps[programListIndex][0]].steps_to_volume(
                    self.programSteps[programListIndex][2][0]))

        elif programCommand == "set_syringe_speed":
            tableCommandParameters.append("Syringe speed index: %s" % self.programSteps[programListIndex][2][0])

        elif programCommand in ["empty_syringe", "fill_syringe"]:
            tableCommandParameters.append("Speed [steps/s]: %s" % self.programSteps[programListIndex][2][2])
            tableCommandParameters.append(
                "Speed [ul/s]: %.2f" % self.deviceList[self.programSteps[programListIndex][0]].steps_to_volume(
                    self.programSteps[programListIndex][2][2]))
            tableCommandParameters.append("Acceleration: %s" % self.programSteps[programListIndex][2][3])
            tableCommandParameters.append("Start velocity: %s" % self.programSteps[programListIndex][2][0])
            tableCommandParameters.append("Stop velocity: %s" % self.programSteps[programListIndex][2][1])

        elif programCommand in ["move_syringe_up", "move_syringe_down"]:
            tableCommandParameters.append("Port: %s" % self.programSteps[programListIndex][2][0])
            tableCommandParameters.append("Steps: %s" % self.programSteps[programListIndex][2][1])
            tableCommandParameters.append(
                "Volume [ul]: %.2f" % self.deviceList[self.programSteps[programListIndex][0]].steps_to_volume(
                    self.programSteps[programListIndex][2][1]))
            tableCommandParameters.append("Speed [steps/s]: %s" % self.programSteps[programListIndex][2][4])
            tableCommandParameters.append(
                "Speed [ul/s]: %.2f" % self.deviceList[self.programSteps[programListIndex][0]].steps_to_volume(
                    self.programSteps[programListIndex][2][4]))
            tableCommandParameters.append("Acceleration: %s" % self.programSteps[programListIndex][2][5])
            tableCommandParameters.append("Start velocity: %s" % self.programSteps[programListIndex][2][2])
            tableCommandParameters.append("Stop velocity: %s" % self.programSteps[programListIndex][2][3])

        # insert/edit row in program table (device ID + device Name; Command; command parameters)
        if Editing == True:
            self.tableProgram.removeRow(programListIndex)

        rowPosition = programListIndex

        self.tableProgram.insertRow(rowPosition)
        rowItem = QtWidgets.QTableWidgetItem(str(self.programSteps[programListIndex][0] + 1) + " - " + self.deviceList[
            self.programSteps[programListIndex][0]].hw_type)
        rowItem.setTextAlignment(QtCore.Qt.AlignLeft)
        if programCommand == "insert_loop_start" or programCommand == "insert_loop_end": rowItem.setBackground(
            QtGui.QColor(125, 125, 125))
        self.tableProgram.setItem(rowPosition, 0, rowItem)
        rowItem = QtWidgets.QTableWidgetItem(programCommand)
        rowItem.setTextAlignment(QtCore.Qt.AlignLeft)
        if programCommand == "insert_loop_start" or programCommand == "insert_loop_end": rowItem.setBackground(
            QtGui.QColor(125, 125, 125))
        self.tableProgram.setItem(rowPosition, 1, rowItem)
        rowItem = QtWidgets.QTableWidgetItem("; ".join(tableCommandParameters))
        rowItem.setTextAlignment(QtCore.Qt.AlignLeft)
        if programCommand == "insert_loop_start" or programCommand == "insert_loop_end": rowItem.setBackground(
            QtGui.QColor(125, 125, 125))
        self.tableProgram.setItem(rowPosition, 2, rowItem)
        QtWidgets.QTableWidget.resizeColumnsToContents(self.tableProgram)
        QtWidgets.QTableWidget.resizeRowsToContents(self.tableProgram)

        if len(self.programSteps) >= 1:
            self.buttonProgramStepRemove.setEnabled(True)
            self.buttonProgramStepEdit.setEnabled(True)
            self.buttonRun.setEnabled(True)
            self.buttonRunSingleCommand.setEnabled(True)
            self.buttonSave.setEnabled(True)

    def clickButtonProgramStepRemove(self):
        stepToRemove = self.tableProgram.currentRow()

        if stepToRemove == -1:
            QtWidgets.QMessageBox.critical(self, 'Error', "Please, select a program step form the list.",
                                           QMessageBox.Ok)
            return

        self.tableProgram.removeRow(stepToRemove)
        self.programSteps.pop(stepToRemove)
        if len(self.programSteps) < 1:
            self.buttonProgramStepRemove.setEnabled(False)
            self.buttonProgramStepEdit.setEnabled(False)
            self.buttonRun.setEnabled(False)
            self.buttonRunSingleCommand.setEnabled(False)
            self.buttonSave.setEnabled(False)

    def clickButtonSave(self):
        # save file dialog
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                            "PSD/MVP program Files (*.prg)", options=options)
        if fileName:
            if ".prg" not in fileName:
                fileName += ".prg"

            # save devices program
            with open(fileName, 'w') as file_to_save:
                file_to_save.write("[Devices]\n")
                for device in self.deviceList:
                    if type(device).__name__ == "PSDpump":
                        file_to_save.write("PSDpump, %s, %s, %s, %s, %s\n" % (
                            device.hw_type, device.hw_address, device.com_port, device.hi_res, device.syringe_volume))
                    elif type(device).__name__ == "MVPvalve":
                        file_to_save.write(
                            "MVPvalve, %s, %s, %s\n" % (device.hw_type, device.hw_address, device.com_port))
                file_to_save.write("[Program]\n")
                for program_step in self.programSteps:
                    file_to_save.write("%s, %s" % (program_step[0], program_step[1]))
                    for program_step_param_item in program_step[2]:
                        file_to_save.write(", %s" % program_step_param_item)
                    file_to_save.write("\n")
        else:
            return

    def clickButtonOpen(self):

        if self.tableDevices.rowCount() > 0 or self.tableProgram.rowCount() > 0:
            reply = QMessageBox.question(self, 'Warning!', "Do you want to rewrite current device and program list?",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.No:
                return

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                            "PSD/MVP program Files (*.prg)", options=options)
        if fileName:
            # clear devicelist and programSteps
            self.deviceList = []
            self.programSteps = []
            # clear tables
            self.tableDevices.setRowCount(0)
            self.tableProgram.setRowCount(0)

            # parse input file
            program_file = open(fileName, 'r')
            count = 0

            line = program_file.readline().strip("\n")

            while True:
                count += 1
                commandParameters = []

                if "[Devices]" in line:
                    while line != "[Program]":
                        # add device
                        device = line.split(", ")
                        if "PSD" in device[0] or "MVP" in device[0]:
                            deviceComPort = device[3]
                            # check if comport is already in use by other device (if so nest them)
                            for deviceFromList in self.deviceList:
                                if deviceFromList.com_port == device[3]:
                                    deviceComPort = deviceFromList.com_interface
                                    break

                        if "PSD" in device[0]:
                            self.deviceList.append(
                                PSDpump(device[1],
                                        device[2], deviceComPort,
                                        device[4] == "True", device[5]))
                            self.deviceTableInsertRow(len(self.deviceList) - 1)
                        elif "MVP" in device[0]:
                            self.deviceList.append(
                                MVPvalve(device[1], device[2], deviceComPort))
                            self.deviceTableInsertRow(len(self.deviceList) - 1)
                        line = program_file.readline().strip("\n")
                # read program lines
                if "[Program]" not in line:
                    program_step = line.split(", ")
                    deviceID = int(program_step.pop(0))
                    programCommand = program_step.pop(0)
                    for command_param in program_step:
                        if command_param.isdigit() or command_param == "-1":
                            commandParameters.append(int(command_param))
                        else:
                            commandParameters.append(command_param)
                    self.programSteps.append([deviceID, programCommand, commandParameters])
                    self.programTableInsertEditRow(len(self.programSteps) - 1)

                line = program_file.readline().strip("\n")
                if not line:
                    break
            program_file.close()

    def clickButtonDeviceAdd(self):
        com_ports = serial.tools.list_ports.comports(include_links=False)

        if len(com_ports) == 0:
            QtWidgets.QMessageBox.critical(self, 'Error', "No COM port was detected on computer!", QMessageBox.Ok)
            return
        else:
            d = DialogAddDevice(self, com_ports)
            result = d.exec()

        if result:
            # check if com port already in use with other device, if yes nest the new device under it
            for device in self.deviceList:
                if device.com_port == d.comboBoxCOMport.currentText():
                    # nest the device
                    if "PSD" in d.comboBoxDevice.currentText():
                        self.deviceList.append(
                            PSDpump(d.comboBoxDevice.currentText() + d.comboBoxDeviceType.currentText(),
                                    d.comboBoxHWaddress.currentText(), device.com_interface,
                                    d.checkBoxHiRes.isChecked(), d.comboBoxSyringe.currentText()))
                    elif "MVP" in d.comboBoxDevice.currentText():
                        self.deviceList.append(
                            MVPvalve(d.comboBoxDevice.currentText(), d.comboBoxHWaddress.currentText(),
                                     device.com_interface))
                self.deviceTableInsertRow(len(self.deviceList) - 1)
                return

            if "PSD" in d.comboBoxDevice.currentText():
                self.deviceList.append(PSDpump(d.comboBoxDevice.currentText() + d.comboBoxDeviceType.currentText(),
                                               d.comboBoxHWaddress.currentText(), d.comboBoxCOMport.currentText(),
                                               d.checkBoxHiRes.isChecked(), d.comboBoxSyringe.currentText()))
            elif "MVP" in d.comboBoxDevice.currentText():
                self.deviceList.append(MVPvalve(d.comboBoxDevice.currentText(), d.comboBoxHWaddress.currentText(),
                                                d.comboBoxCOMport.currentText()))

            self.deviceTableInsertRow(len(self.deviceList) - 1)

    def deviceTableInsertRow(self, deviceListIndex):
        rowPosition = self.tableDevices.rowCount()
        self.tableDevices.insertRow(rowPosition)
        rowItem = QtWidgets.QTableWidgetItem(self.deviceList[deviceListIndex].hw_type)
        rowItem.setTextAlignment(QtCore.Qt.AlignLeft)
        self.tableDevices.setItem(rowPosition, 0, rowItem)
        rowItem = QtWidgets.QTableWidgetItem(self.deviceList[deviceListIndex].hw_address)
        rowItem.setTextAlignment(QtCore.Qt.AlignRight)
        self.tableDevices.setItem(rowPosition, 1, rowItem)
        rowItem = QtWidgets.QTableWidgetItem(self.deviceList[deviceListIndex].com_port)
        rowItem.setTextAlignment(QtCore.Qt.AlignLeft)
        self.tableDevices.setItem(rowPosition, 2, rowItem)
        if "PSD" in self.deviceList[deviceListIndex].hw_type:
            rowItem = QtWidgets.QTableWidgetItem(str(self.deviceList[deviceListIndex].syringe_volume))
            rowItem.setTextAlignment(QtCore.Qt.AlignRight)
            self.tableDevices.setItem(rowPosition, 3, rowItem)
            if self.deviceList[deviceListIndex].hi_res:
                rowItem = QtWidgets.QTableWidgetItem("Yes")
            else:
                rowItem = QtWidgets.QTableWidgetItem("No")
            rowItem.setTextAlignment(QtCore.Qt.AlignLeft)
            self.tableDevices.setItem(rowPosition, 4, rowItem)
        QtWidgets.QTableWidget.resizeColumnsToContents(self.tableDevices)
        QtWidgets.QTableWidget.resizeRowsToContents(self.tableDevices)

        if len(self.deviceList) > 0:
            self.buttonDeviceRemove.setEnabled(True)

    def clickButtonDevicesRemove(self):
        deviceToRemove = self.tableDevices.currentRow()
        if deviceToRemove == -1:
            QtWidgets.QMessageBox.critical(self, 'Error', "Please, select a device form the list.", QMessageBox.Ok)
            return

        for step in self.programSteps:
            if step[0] == deviceToRemove:
                QtWidgets.QMessageBox.warning(self, 'Warning',
                                              "You cannot remove a device already in use in the program",
                                              QMessageBox.Ok)
                return

        self.tableDevices.removeRow(deviceToRemove)
        self.deviceList.pop(deviceToRemove)
        if len(self.deviceList) < 1:
            self.buttonDeviceRemove.setEnabled(False)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()

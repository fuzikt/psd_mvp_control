# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_program_step.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogAddProgramStep(object):
    def setupUi(self, DialogAddProgramStep):
        DialogAddProgramStep.setObjectName("DialogAddProgramStep")
        DialogAddProgramStep.resize(605, 343)
        self.gridLayout_4 = QtWidgets.QGridLayout(DialogAddProgramStep)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelDevice = QtWidgets.QLabel(DialogAddProgramStep)
        self.labelDevice.setObjectName("labelDevice")
        self.gridLayout_4.addWidget(self.labelDevice, 0, 0, 1, 1)
        self.labelBasicCommand = QtWidgets.QLabel(DialogAddProgramStep)
        self.labelBasicCommand.setObjectName("labelBasicCommand")
        self.gridLayout_4.addWidget(self.labelBasicCommand, 0, 1, 1, 1)
        self.labelComplexCommand = QtWidgets.QLabel(DialogAddProgramStep)
        self.labelComplexCommand.setObjectName("labelComplexCommand")
        self.gridLayout_4.addWidget(self.labelComplexCommand, 0, 2, 1, 1)
        self.comboBoxDevice = QtWidgets.QComboBox(DialogAddProgramStep)
        self.comboBoxDevice.setObjectName("comboBoxDevice")
        self.gridLayout_4.addWidget(self.comboBoxDevice, 1, 0, 1, 1)
        self.comboBoxBasicCommands = QtWidgets.QComboBox(DialogAddProgramStep)
        self.comboBoxBasicCommands.setObjectName("comboBoxBasicCommands")
        self.gridLayout_4.addWidget(self.comboBoxBasicCommands, 1, 1, 1, 1)
        self.groupBoxValve = QtWidgets.QGroupBox(DialogAddProgramStep)
        self.groupBoxValve.setEnabled(False)
        self.groupBoxValve.setObjectName("groupBoxValve")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxValve)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.radioButtonOutputLeft = QtWidgets.QRadioButton(self.groupBoxValve)
        self.radioButtonOutputLeft.setChecked(True)
        self.radioButtonOutputLeft.setObjectName("radioButtonOutputLeft")
        self.gridLayout_3.addWidget(self.radioButtonOutputLeft, 0, 0, 1, 2)
        self.radioButtonOutputRight = QtWidgets.QRadioButton(self.groupBoxValve)
        self.radioButtonOutputRight.setObjectName("radioButtonOutputRight")
        self.gridLayout_3.addWidget(self.radioButtonOutputRight, 1, 0, 1, 2)
        self.labelValvePort = QtWidgets.QLabel(self.groupBoxValve)
        self.labelValvePort.setObjectName("labelValvePort")
        self.gridLayout_3.addWidget(self.labelValvePort, 2, 0, 1, 1)
        self.spinBoxValvePort = QtWidgets.QSpinBox(self.groupBoxValve)
        self.spinBoxValvePort.setMinimum(-1)
        self.spinBoxValvePort.setMaximum(8)
        self.spinBoxValvePort.setProperty("value", -1)
        self.spinBoxValvePort.setObjectName("spinBoxValvePort")
        self.gridLayout_3.addWidget(self.spinBoxValvePort, 2, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxValve, 2, 0, 1, 1)
        self.groupBoxSetSteps = QtWidgets.QGroupBox(DialogAddProgramStep)
        self.groupBoxSetSteps.setEnabled(False)
        self.groupBoxSetSteps.setObjectName("groupBoxSetSteps")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxSetSteps)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBoxSetSteps)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.spinBoxVolume = QtWidgets.QDoubleSpinBox(self.groupBoxSetSteps)
        self.spinBoxVolume.setObjectName("spinBoxVolume")
        self.gridLayout_2.addWidget(self.spinBoxVolume, 1, 1, 1, 1)
        self.spinBoxSteps = QtWidgets.QSpinBox(self.groupBoxSetSteps)
        self.spinBoxSteps.setToolTip("")
        self.spinBoxSteps.setReadOnly(False)
        self.spinBoxSteps.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinBoxSteps.setObjectName("spinBoxSteps")
        self.gridLayout_2.addWidget(self.spinBoxSteps, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBoxSetSteps)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxSetSteps, 2, 1, 1, 1)
        self.groupBoxPumpSpeed = QtWidgets.QGroupBox(DialogAddProgramStep)
        self.groupBoxPumpSpeed.setEnabled(False)
        self.groupBoxPumpSpeed.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBoxPumpSpeed.setObjectName("groupBoxPumpSpeed")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxPumpSpeed)
        self.gridLayout.setObjectName("gridLayout")
        self.labelSpeedSteps = QtWidgets.QLabel(self.groupBoxPumpSpeed)
        self.labelSpeedSteps.setObjectName("labelSpeedSteps")
        self.gridLayout.addWidget(self.labelSpeedSteps, 0, 0, 1, 3)
        self.spinBoxSpeedSteps = QtWidgets.QSpinBox(self.groupBoxPumpSpeed)
        self.spinBoxSpeedSteps.setObjectName("spinBoxSpeedSteps")
        self.gridLayout.addWidget(self.spinBoxSpeedSteps, 0, 3, 1, 1)
        self.labelAcceleration = QtWidgets.QLabel(self.groupBoxPumpSpeed)
        self.labelAcceleration.setObjectName("labelAcceleration")
        self.gridLayout.addWidget(self.labelAcceleration, 0, 4, 1, 1)
        self.spinBoxAcceleration = QtWidgets.QSpinBox(self.groupBoxPumpSpeed)
        self.spinBoxAcceleration.setObjectName("spinBoxAcceleration")
        self.gridLayout.addWidget(self.spinBoxAcceleration, 0, 5, 1, 1)
        self.labelSpeedVolume = QtWidgets.QLabel(self.groupBoxPumpSpeed)
        self.labelSpeedVolume.setObjectName("labelSpeedVolume")
        self.gridLayout.addWidget(self.labelSpeedVolume, 1, 0, 1, 1)
        self.spinBoxSpeedVolume = QtWidgets.QDoubleSpinBox(self.groupBoxPumpSpeed)
        self.spinBoxSpeedVolume.setObjectName("spinBoxSpeedVolume")
        self.gridLayout.addWidget(self.spinBoxSpeedVolume, 1, 1, 1, 3)
        self.labelStartVelocity = QtWidgets.QLabel(self.groupBoxPumpSpeed)
        self.labelStartVelocity.setObjectName("labelStartVelocity")
        self.gridLayout.addWidget(self.labelStartVelocity, 1, 4, 1, 1)
        self.spinBoxStartVelocity = QtWidgets.QSpinBox(self.groupBoxPumpSpeed)
        self.spinBoxStartVelocity.setObjectName("spinBoxStartVelocity")
        self.gridLayout.addWidget(self.spinBoxStartVelocity, 1, 5, 1, 1)
        self.labelSpeedSyringe = QtWidgets.QLabel(self.groupBoxPumpSpeed)
        self.labelSpeedSyringe.setObjectName("labelSpeedSyringe")
        self.gridLayout.addWidget(self.labelSpeedSyringe, 2, 0, 1, 2)
        self.spinBoxSpeedSyringe = QtWidgets.QSpinBox(self.groupBoxPumpSpeed)
        self.spinBoxSpeedSyringe.setObjectName("spinBoxSpeedSyringe")
        self.gridLayout.addWidget(self.spinBoxSpeedSyringe, 2, 2, 1, 2)
        self.labelStopVelocity = QtWidgets.QLabel(self.groupBoxPumpSpeed)
        self.labelStopVelocity.setObjectName("labelStopVelocity")
        self.gridLayout.addWidget(self.labelStopVelocity, 2, 4, 1, 1)
        self.spinBoxStopVelocity = QtWidgets.QSpinBox(self.groupBoxPumpSpeed)
        self.spinBoxStopVelocity.setObjectName("spinBoxStopVelocity")
        self.gridLayout.addWidget(self.spinBoxStopVelocity, 2, 5, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxPumpSpeed, 2, 2, 1, 3)
        self.labelDescription = QtWidgets.QLabel(DialogAddProgramStep)
        self.labelDescription.setObjectName("labelDescription")
        self.gridLayout_4.addWidget(self.labelDescription, 3, 0, 1, 1)
        self.textEditDescription = QtWidgets.QTextEdit(DialogAddProgramStep)
        self.textEditDescription.setEnabled(True)
        self.textEditDescription.setReadOnly(True)
        self.textEditDescription.setObjectName("textEditDescription")
        self.gridLayout_4.addWidget(self.textEditDescription, 4, 0, 1, 5)
        self.labelHInt = QtWidgets.QLabel(DialogAddProgramStep)
        self.labelHInt.setObjectName("labelHInt")
        self.gridLayout_4.addWidget(self.labelHInt, 5, 0, 1, 3)
        self.comboBoxComplexCommands = QtWidgets.QComboBox(DialogAddProgramStep)
        self.comboBoxComplexCommands.setObjectName("comboBoxComplexCommands")
        self.gridLayout_4.addWidget(self.comboBoxComplexCommands, 1, 2, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogAddProgramStep)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_4.addWidget(self.buttonBox, 1, 4, 1, 1)

        self.retranslateUi(DialogAddProgramStep)
        self.buttonBox.accepted.connect(DialogAddProgramStep.accept)
        self.buttonBox.rejected.connect(DialogAddProgramStep.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAddProgramStep)

    def retranslateUi(self, DialogAddProgramStep):
        _translate = QtCore.QCoreApplication.translate
        DialogAddProgramStep.setWindowTitle(_translate("DialogAddProgramStep", "Add Program Step"))
        self.labelDevice.setText(_translate("DialogAddProgramStep", "Device"))
        self.labelBasicCommand.setText(_translate("DialogAddProgramStep", "Basic command"))
        self.labelComplexCommand.setText(_translate("DialogAddProgramStep", "Complex command"))
        self.groupBoxValve.setTitle(_translate("DialogAddProgramStep", "Valve"))
        self.radioButtonOutputLeft.setText(_translate("DialogAddProgramStep", "Output Left"))
        self.radioButtonOutputRight.setText(_translate("DialogAddProgramStep", "Output Right"))
        self.labelValvePort.setText(_translate("DialogAddProgramStep", "Valve port:"))
        self.groupBoxSetSteps.setTitle(_translate("DialogAddProgramStep", "Set steps"))
        self.label_3.setText(_translate("DialogAddProgramStep", "Steps"))
        self.label_4.setText(_translate("DialogAddProgramStep", "Volume [ul]"))
        self.groupBoxPumpSpeed.setTitle(_translate("DialogAddProgramStep", "Pump speed"))
        self.labelSpeedSteps.setText(_translate("DialogAddProgramStep", "Speed [steps/s]"))
        self.labelAcceleration.setText(_translate("DialogAddProgramStep", "Acceleration"))
        self.labelSpeedVolume.setText(_translate("DialogAddProgramStep", "Speed [ul/s]"))
        self.labelStartVelocity.setText(_translate("DialogAddProgramStep", "Start velocity"))
        self.labelSpeedSyringe.setText(_translate("DialogAddProgramStep", "Syringe speed"))
        self.labelStopVelocity.setText(_translate("DialogAddProgramStep", "Stop velocity"))
        self.labelDescription.setText(_translate("DialogAddProgramStep", "Command description"))
        self.labelHInt.setText(_translate("DialogAddProgramStep", "Hint: Hover over the boxes to see the range of allowed values"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogAddProgramStep = QtWidgets.QDialog()
    ui = Ui_DialogAddProgramStep()
    ui.setupUi(DialogAddProgramStep)
    DialogAddProgramStep.show()
    sys.exit(app.exec_())

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

from gui.add_device import Ui_DialogAddDevice

class DialogAddDevice(QtWidgets.QDialog, Ui_DialogAddDevice):
    def __init__(self, parent=None, com_port_list=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.comboBoxDevice.currentTextChanged.connect(self.comboBoxDeviceTypeChanged)

        for port in com_port_list:
            self.comboBoxCOMport.addItem(port.device)

    def comboBoxDeviceTypeChanged(self,value):
        if value == "PSD/4":
            self.comboBoxSyringe.setEnabled(True)
            self.comboBoxDeviceType.setEnabled(True)
            self.checkBoxHiRes.setEnabled(True)
            self.comboBoxDeviceType.addItems(["STD", "SF", "HLF", "HVT", "HLF/HVT"])
            self.comboBoxSyringe.clear()
            self.comboBoxSyringe.addItems(["12.5","25","50","100","125","250","500","1000","1250","2500","5000","12500"])
        elif value == "PSD/6":
            self.comboBoxSyringe.setEnabled(True)
            self.comboBoxDeviceType.setEnabled(True)
            self.checkBoxHiRes.setEnabled(True)
            self.comboBoxDeviceType.addItems(["STD", "SF", "HLF", "HVT", "HLF/HVT"])
            self.comboBoxSyringe.clear()
            self.comboBoxSyringe.addItems(["25", "50", "100", "250", "500", "1000","2500","5000","10000","25000","50000"])
        elif value == "MVP/4":
            self.labelType.setEnabled(False)
            self.comboBoxDeviceType.setEnabled(False)
            self.comboBoxDeviceType.clear()
            self.labelSyringe.setEnabled(False)
            self.comboBoxSyringe.setEnabled(False)
            self.comboBoxSyringe.clear()
            self.checkBoxHiRes.setEnabled(False)
            self.checkBoxHiRes.setChecked(False)
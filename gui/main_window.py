# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(778, 705)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBoxDevices = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxDevices.setObjectName("groupBoxDevices")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxDevices)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonComLog = QtWidgets.QPushButton(self.groupBoxDevices)
        self.buttonComLog.setObjectName("buttonComLog")
        self.gridLayout.addWidget(self.buttonComLog, 3, 2, 1, 1)
        self.tableDevices = QtWidgets.QTableWidget(self.groupBoxDevices)
        self.tableDevices.setObjectName("tableDevices")
        self.tableDevices.setColumnCount(0)
        self.tableDevices.setRowCount(0)
        self.gridLayout.addWidget(self.tableDevices, 0, 1, 5, 1)
        self.buttonDeviceAdd = QtWidgets.QPushButton(self.groupBoxDevices)
        self.buttonDeviceAdd.setObjectName("buttonDeviceAdd")
        self.gridLayout.addWidget(self.buttonDeviceAdd, 0, 2, 1, 1)
        self.buttonDeviceRemove = QtWidgets.QPushButton(self.groupBoxDevices)
        self.buttonDeviceRemove.setEnabled(False)
        self.buttonDeviceRemove.setObjectName("buttonDeviceRemove")
        self.gridLayout.addWidget(self.buttonDeviceRemove, 1, 2, 1, 1)
        self.labelSpacer3 = QtWidgets.QLabel(self.groupBoxDevices)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSpacer3.sizePolicy().hasHeightForWidth())
        self.labelSpacer3.setSizePolicy(sizePolicy)
        self.labelSpacer3.setText("")
        self.labelSpacer3.setObjectName("labelSpacer3")
        self.gridLayout.addWidget(self.labelSpacer3, 2, 2, 1, 1)
        self.gridLayout_3.addWidget(self.groupBoxDevices, 0, 0, 1, 1)
        self.groupBoxProgram = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxProgram.setObjectName("groupBoxProgram")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxProgram)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.buttonStop = QtWidgets.QPushButton(self.groupBoxProgram)
        self.buttonStop.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonStop.sizePolicy().hasHeightForWidth())
        self.buttonStop.setSizePolicy(sizePolicy)
        self.buttonStop.setObjectName("buttonStop")
        self.gridLayout_2.addWidget(self.buttonStop, 8, 1, 1, 1)
        self.buttonOpen = QtWidgets.QPushButton(self.groupBoxProgram)
        self.buttonOpen.setObjectName("buttonOpen")
        self.gridLayout_2.addWidget(self.buttonOpen, 3, 1, 1, 1)
        self.buttonProgramStepRemove = QtWidgets.QPushButton(self.groupBoxProgram)
        self.buttonProgramStepRemove.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonProgramStepRemove.sizePolicy().hasHeightForWidth())
        self.buttonProgramStepRemove.setSizePolicy(sizePolicy)
        self.buttonProgramStepRemove.setObjectName("buttonProgramStepRemove")
        self.gridLayout_2.addWidget(self.buttonProgramStepRemove, 1, 1, 1, 1)
        self.labelSpacer1 = QtWidgets.QLabel(self.groupBoxProgram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSpacer1.sizePolicy().hasHeightForWidth())
        self.labelSpacer1.setSizePolicy(sizePolicy)
        self.labelSpacer1.setText("")
        self.labelSpacer1.setObjectName("labelSpacer1")
        self.gridLayout_2.addWidget(self.labelSpacer1, 2, 1, 1, 1)
        self.tableProgram = QtWidgets.QTableWidget(self.groupBoxProgram)
        self.tableProgram.setObjectName("tableProgram")
        self.tableProgram.setColumnCount(0)
        self.tableProgram.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableProgram, 0, 0, 14, 1)
        self.labelSpacer = QtWidgets.QLabel(self.groupBoxProgram)
        self.labelSpacer.setText("")
        self.labelSpacer.setObjectName("labelSpacer")
        self.gridLayout_2.addWidget(self.labelSpacer, 9, 1, 1, 1)
        self.buttonRun = QtWidgets.QPushButton(self.groupBoxProgram)
        self.buttonRun.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonRun.sizePolicy().hasHeightForWidth())
        self.buttonRun.setSizePolicy(sizePolicy)
        self.buttonRun.setObjectName("buttonRun")
        self.gridLayout_2.addWidget(self.buttonRun, 7, 1, 1, 1)
        self.buttonRunSingleCommand = QtWidgets.QPushButton(self.groupBoxProgram)
        self.buttonRunSingleCommand.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonRunSingleCommand.sizePolicy().hasHeightForWidth())
        self.buttonRunSingleCommand.setSizePolicy(sizePolicy)
        self.buttonRunSingleCommand.setObjectName("buttonRunSingleCommand")
        self.gridLayout_2.addWidget(self.buttonRunSingleCommand, 6, 1, 1, 1)
        self.labelRepeats = QtWidgets.QLabel(self.groupBoxProgram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRepeats.sizePolicy().hasHeightForWidth())
        self.labelRepeats.setSizePolicy(sizePolicy)
        self.labelRepeats.setObjectName("labelRepeats")
        self.gridLayout_2.addWidget(self.labelRepeats, 12, 1, 1, 1)
        self.labelInfo = QtWidgets.QLabel(self.groupBoxProgram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfo.sizePolicy().hasHeightForWidth())
        self.labelInfo.setSizePolicy(sizePolicy)
        self.labelInfo.setObjectName("labelInfo")
        self.gridLayout_2.addWidget(self.labelInfo, 11, 1, 1, 1)
        self.buttonSave = QtWidgets.QPushButton(self.groupBoxProgram)
        self.buttonSave.setEnabled(False)
        self.buttonSave.setObjectName("buttonSave")
        self.gridLayout_2.addWidget(self.buttonSave, 4, 1, 1, 1)
        self.labelRepeatStatus = QtWidgets.QLabel(self.groupBoxProgram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRepeatStatus.sizePolicy().hasHeightForWidth())
        self.labelRepeatStatus.setSizePolicy(sizePolicy)
        self.labelRepeatStatus.setObjectName("labelRepeatStatus")
        self.gridLayout_2.addWidget(self.labelRepeatStatus, 13, 1, 1, 1)
        self.labelStatus = QtWidgets.QLabel(self.groupBoxProgram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus.sizePolicy().hasHeightForWidth())
        self.labelStatus.setSizePolicy(sizePolicy)
        self.labelStatus.setObjectName("labelStatus")
        self.gridLayout_2.addWidget(self.labelStatus, 10, 1, 1, 1)
        self.buttonProgramStepAdd = QtWidgets.QPushButton(self.groupBoxProgram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonProgramStepAdd.sizePolicy().hasHeightForWidth())
        self.buttonProgramStepAdd.setSizePolicy(sizePolicy)
        self.buttonProgramStepAdd.setObjectName("buttonProgramStepAdd")
        self.gridLayout_2.addWidget(self.buttonProgramStepAdd, 0, 1, 1, 1)
        self.labelSpacer2 = QtWidgets.QLabel(self.groupBoxProgram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSpacer2.sizePolicy().hasHeightForWidth())
        self.labelSpacer2.setSizePolicy(sizePolicy)
        self.labelSpacer2.setText("")
        self.labelSpacer2.setObjectName("labelSpacer2")
        self.gridLayout_2.addWidget(self.labelSpacer2, 5, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBoxProgram, 1, 0, 1, 3)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("logo_plevkalab.png"))
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)
        self.gridLayout_3.setRowStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PSD / MVP controller"))
        self.groupBoxDevices.setTitle(_translate("MainWindow", "Devices"))
        self.buttonComLog.setText(_translate("MainWindow", "COM log"))
        self.buttonDeviceAdd.setText(_translate("MainWindow", "Add..."))
        self.buttonDeviceRemove.setText(_translate("MainWindow", "Remove"))
        self.groupBoxProgram.setTitle(_translate("MainWindow", "Program"))
        self.buttonStop.setText(_translate("MainWindow", "Stop"))
        self.buttonOpen.setText(_translate("MainWindow", "Open program..."))
        self.buttonProgramStepRemove.setText(_translate("MainWindow", "Remove"))
        self.buttonRun.setText(_translate("MainWindow", "Run program"))
        self.buttonRunSingleCommand.setText(_translate("MainWindow", "Run step"))
        self.labelRepeats.setText(_translate("MainWindow", "Loop repeats"))
        self.labelInfo.setText(_translate("MainWindow", "-"))
        self.buttonSave.setText(_translate("MainWindow", "Save program..."))
        self.labelRepeatStatus.setText(_translate("MainWindow", "-/-"))
        self.labelStatus.setText(_translate("MainWindow", "Device status:"))
        self.buttonProgramStepAdd.setText(_translate("MainWindow", "Add..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'com_log.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogComLog(object):
    def setupUi(self, DialogComLog):
        DialogComLog.setObjectName("DialogComLog")
        DialogComLog.resize(377, 307)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogComLog.sizePolicy().hasHeightForWidth())
        DialogComLog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(DialogComLog)
        self.gridLayout.setObjectName("gridLayout")
        self.comunicationLogList = QtWidgets.QListWidget(DialogComLog)
        self.comunicationLogList.setObjectName("comunicationLogList")
        self.gridLayout.addWidget(self.comunicationLogList, 0, 0, 2, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogComLog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 0, 1, 1, 1)
        self.buttonClear = QtWidgets.QPushButton(DialogComLog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonClear.sizePolicy().hasHeightForWidth())
        self.buttonClear.setSizePolicy(sizePolicy)
        self.buttonClear.setObjectName("buttonClear")
        self.gridLayout.addWidget(self.buttonClear, 1, 1, 1, 1)

        self.retranslateUi(DialogComLog)
        self.buttonBox.accepted.connect(DialogComLog.accept)
        self.buttonBox.rejected.connect(DialogComLog.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogComLog)

    def retranslateUi(self, DialogComLog):
        _translate = QtCore.QCoreApplication.translate
        DialogComLog.setWindowTitle(_translate("DialogComLog", "Device communication"))
        self.buttonClear.setText(_translate("DialogComLog", "Clear Log"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogComLog = QtWidgets.QDialog()
    ui = Ui_DialogComLog()
    ui.setupUi(DialogComLog)
    DialogComLog.show()
    sys.exit(app.exec_())

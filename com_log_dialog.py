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

from gui.com_log import Ui_DialogComLog


class DialogComLog(QtWidgets.QDialog, Ui_DialogComLog):
    def __init__(self, parent=None, com_port_list=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        #EVENTS
        self.buttonClear.clicked.connect(self.ButtonClear)

    def ButtonClear(self):
        self.comunicationLogList.clear()
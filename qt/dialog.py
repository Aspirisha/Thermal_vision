# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Mon Nov  9 19:20:19 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from dialog_ui import Ui_Dialog
import sys

class ControlDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ControlDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def ok_pressed():
        pass

qtapp = QtGui.QApplication(sys.argv)
dlg = ControlDialog()
dlg.show()
qtapp.exec_()
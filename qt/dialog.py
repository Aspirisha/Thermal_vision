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

def show_all_widgets_in_layout(layout, show):
    items = (layout.itemAt(i) for i in range(layout.count())) 
    for item in items:
        if item.widget() is not None:
            item.widget().hide()
        if item.layout():
            show_all_widgets_in_layout(item.layout(), show)

class ControlDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ControlDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        show_all_widgets_in_layout(self.ui.by_name_options_layout, False)
        self.ui.gridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        #self.ui.gridLayout.adjustSize()

    def ok_pressed():
        pass

def main():
    qtapp = QtGui.QApplication(sys.argv)
    dlg = ControlDialog()
    dlg.show()
    qtapp.exec_()

if __name__ == '__main__':
    main()
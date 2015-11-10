# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Mon Nov  9 19:20:19 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from dialog_ui import Ui_Dialog
import PyQt4
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
        self.setLayout(self.ui.gridLayout)
       
        self.ui.groupBox_3.setEnabled(False)

        self.rgb_combobox = QtGui.QComboBox(self)
        self.ui.rgb_tv_table.setCellWidget(0,0,self.rgb_combobox)

        self.tv_combobox = QtGui.QComboBox(self)
        self.ui.rgb_tv_table.setCellWidget(0,1,self.tv_combobox)
        self.rgb_calib_photos_are_ok = False
        self.tv_calib_photos_are_ok = False

    def ok_pressed(self):
        pass

    def save_matrices_to_file_checked(self, checked):
        pass

    def use_matrices_from_file_clicked(self):
        pass

    def calculate_matrices_radio_clicked(self):
        self.ui.groupBox_2.setEnabled(True)
        self.ui.groupBox_3.setEnabled(False)
        pass

    def select_matrices_radio_clicked(self):
        self.ui.groupBox_3.setEnabled(True)
        self.ui.groupBox_2.setEnabled(False)
        pass

    def select_rgb_calib_files_cliked(self):
        files = QtGui.QFileDialog.getOpenFileNames(
                        self,
                        "Select one or more files to open",
                        "/home/andy/AU/Geoscan/",
                        "Images (*.png *.xpm *.jpg *.bmp)")[0];
        print("You chose: " + str(files))
        if len(files) > MIN_CALIBRATION_FILES:
            self.rgb_calibration_files = files
        else:
            pass
        pass

    def select_tv_calib_files_clicked(self):
        pass

    def readonly_checkboxes_checked(self):
        self.ui.rgb_photos_ok_checkbox.setChecked(self.rgb_calib_photos_are_ok)
        self.ui.tv_photos_ok_checkbox.setChecked(self.tv_calib_photos_are_ok)

def main():
    qtapp = QtGui.QApplication(sys.argv)
    dlg = ControlDialog()
    dlg.show()
    qtapp.exec_()

if __name__ == '__main__':
    main()
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
    MIN_CALIBRATION_FILES = 4
    def __init__(self, parent=None):
        super(ControlDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
       
        self.ui.groupBox_3.setEnabled(False)

        self.rgb_checkboxes = []
        #self.ui.rgb_tv_table.setCellWidget(0,0,self.rgb_combobox)
        #self.rgb_checkboxes.currentIndexChanged.connect(self.rgb_)

        self.tv_comboboxes = []
        self.file_name_to_save_matrices = None
        self.tv_calibration_files = None
        self.rgb_calibration_files = None

    def ok_pressed(self):
        pass

    def save_matrices_to_file_checked(self, checked):
        options = QtGui.QFileDialog.Options()
        
        file_name, filtr = QtGui.QFileDialog.getSaveFileName(self,
                "QFileDialog.getSaveFileName()",
                "calibration.txt",
                "All Files (*);;Text Files (*.txt)", "", options)
        self.file_name_to_save_matrices = file_name


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

    def select_calibration_files_clicked(self):
        files = QtGui.QFileDialog.getOpenFileNames(
                        self,
                        "Select one or more files to open",
                        "/home/andy/AU/Geoscan/",
                        "Images (*.png *.xpm *.jpg *.bmp)")[0];
        print("You chose: " + str(files))
        if len(files) > ControlDialog.MIN_CALIBRATION_FILES:
            return files
        else:
            ret = QtGui.QMessageBox.information(self, self.tr("Calibration files"),
                   self.tr("Not enough files for calibration. Should be at least " + str(ControlDialog.MIN_CALIBRATION_FILES)),
                   QtGui.QMessageBox.Ok)

            return None

    def select_rgb_calib_files_cliked(self):
        files = self.select_calibration_files_clicked()
        if files is not None:
            self.rgb_calibration_files = files
            self.readonly_checkboxes_checked()
            self.ui.rgb_tv_table.setRowCount(len(files))
            
            self.rgb_checkboxes = []            
            self.tv_comboboxes = []

            for i, f in enumerate(files):
                new_check_box = QtGui.QCheckBox(self)
                new_check_box.setChecked(False)
                new_check_box.setText(f)
                
                self.rgb_checkboxes.append(new_check_box)
                self.ui.rgb_tv_table.setCellWidget(i,0,new_check_box)
                
                new_combo_box = QtGui.QComboBox(self)
                self.tv_comboboxes.append(new_combo_box)

            if self.tv_calibration_files:
                for cbox in self.tv_comboboxes:
                    cbox.addItems(self.tv_calibration_files)

    def select_tv_calib_files_clicked(self):
        files = self.select_calibration_files_clicked()
        if files is not None:
            self.tv_calibration_files = files
            self.readonly_checkboxes_checked()
            self.tv_combobox.clear()
            self.tv_combobox.addItems(files)

    def readonly_checkboxes_checked(self):
        self.ui.rgb_photos_ok_checkbox.setChecked(self.rgb_calibration_files is not None)
        self.ui.tv_photos_ok_checkbox.setChecked(self.tv_calibration_files is not None)

def main():
    qtapp = QtGui.QApplication(sys.argv)
    dlg = ControlDialog()
    dlg.show()
    qtapp.exec_()

if __name__ == '__main__':
    main()
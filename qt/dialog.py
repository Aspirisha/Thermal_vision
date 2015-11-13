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

sys.path.append("../")
from camera_relative_position import get_tv_to_rgb_matrix
from get_enabled_cameras import build_tv_texture

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
        self.ui.cell_size_edit.setValidator(QtGui.QDoubleValidator(0, 100, 4, self))

        self.rgb_checkboxes = []
        self.tv_comboboxes = []
        self.file_name_to_save_matrices = None
        self.tv_calibration_files = None
        self.rgb_calibration_files = None
        self.rgb_short_file_names = None
        self.tv_short_file_names = None
        self.checked_correpsonfing_photos = 0

    def ok_pressed(self):      
        rgb_images = self.rgb_calibration_files
        tv_images = self.tv_calibration_files
        
        rgb_relative_file_names = []
        tv_relative_file_names = []
        for i, chbox in enumerate(self.rgb_checkboxes):
            if not chbox.isChecked():
                continue
            rgb_relative_file_names.append(self.rgb_calibration_files[i])
            tv_relative_file_names.append(self.tv_calibration_files[i])

        cell_size = float(self.ui.cell_size_edit.text())

        A, cameraMatrix_rgb, distCoeffs_rgb, cameraMatrix_tv, distCoeffs_tv = get_tv_to_rgb_matrix(
            rgb_images, tv_images, rgb_relative_file_names, tv_relative_file_names, cell_size)

        if self.ui.save_matrices_checkbox.isChecked():
            f = open(self.file_name_to_save_matrices)
            f.write(str(cameraMatrix_rgb))
            f.write(str(distCoeffs_rgb))
            f.write(str(cameraMatrix_tv))
            f.write(str(distCoeffs_tv))
            f.write(str(A))

        rgb_time_file = "time_rgb.txt"
        tv_time_file = "time_tv.txt"
        build_tv_texture(A, rgb_time_file, tv_time_file, cameraMatrix_tv, distCoeffs_tv)
        

    def save_matrices_to_file_checked(self, checked):
        options = QtGui.QFileDialog.Options()
        
        file_name, filtr = QtGui.QFileDialog.getSaveFileName(self,
                "QFileDialog.getSaveFileName()",
                "calibration.txt",
                "All Files (*);;Text Files (*.txt)", "", options)
        if file_name is not None:
            self.file_name_to_save_matrices = file_name
        else:
            self.ui.save_matrices_checkbox.setChecked(False)


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
        if len(files) >= ControlDialog.MIN_CALIBRATION_FILES:
            return files
        else:
            ret = QtGui.QMessageBox.information(self, self.tr("Calibration files"),
                   self.tr("Not enough files for calibration. Should be at least " + str(ControlDialog.MIN_CALIBRATION_FILES)),
                   QtGui.QMessageBox.Ok)

            return None

    def update_tv_comboboxes(self):
        for i, cbox in enumerate(self.tv_comboboxes):
            cbox.clear()
            cbox.addItems(self.tv_short_file_names)
            self.rgb_checkboxes[i].stateChanged.connect(cbox.setEnabled)
            self.rgb_checkboxes[i].setEnabled(True)
            

    def select_rgb_calib_files_cliked(self):
        files = self.select_calibration_files_clicked()
        if files is not None:
            self.checked_correpsonfing_photos = 0
            self.rgb_calibration_files = files
            self.readonly_checkboxes_checked()
            self.ui.rgb_tv_table.setRowCount(len(files))
            self.rgb_short_file_names = [s.split('/')[-1] for s in files]

            self.rgb_checkboxes = []            
            self.tv_comboboxes = []

            self.checked_correpsonfing_photos = 0
            for i, f in enumerate(self.rgb_short_file_names):
                new_check_box = QtGui.QCheckBox(self)
                new_check_box.setChecked(False)
                new_check_box.setEnabled(False)
                new_check_box.setText(f)
                new_check_box.stateChanged.connect(self.table_checkbox_clicked)
                
                self.rgb_checkboxes.append(new_check_box)
                self.ui.rgb_tv_table.setCellWidget(i,0,new_check_box)
                
                new_combo_box = QtGui.QComboBox(self)
                self.tv_comboboxes.append(new_combo_box)
                self.ui.rgb_tv_table.setCellWidget(i,1,new_combo_box)
                new_combo_box.setEnabled(False)

            if self.tv_calibration_files:
                self.update_tv_comboboxes()

    def select_tv_calib_files_clicked(self):
        files = self.select_calibration_files_clicked()
        if files is not None:
            self.tv_short_file_names = [s.split('/')[-1] for s in files]
            self.tv_calibration_files = files
            self.readonly_checkboxes_checked()
            self.update_tv_comboboxes()

    def readonly_checkboxes_checked(self):
        self.ui.rgb_photos_ok_checkbox.setChecked(self.rgb_calibration_files is not None)
        self.ui.tv_photos_ok_checkbox.setChecked(self.tv_calibration_files is not None)

    def table_checkbox_clicked(self, checked):
        if checked and self.tv_calibration_files:
            self.ui.ok_button.setEnabled(True)
            self.checked_correpsonfing_photos += 1
        else:
            self.checked_correpsonfing_photos -= 1
            if self.checked_correpsonfing_photos == 0:
                self.ui.ok_button.setEnabled(False)

def main():
    qtapp = QtGui.QApplication(sys.argv)
    dlg = ControlDialog()
    dlg.show()
    qtapp.exec_()

if __name__ == '__main__':
    main()
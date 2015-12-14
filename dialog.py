#/usr/bin/python

import sys
import os
support_directory = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'support'
temp_directory = support_directory + os.sep + '.tmp'
sys.path.append(support_directory)

from PySide import QtCore, QtGui
from dialog_ui import Ui_Dialog
import PhotoScan as ps
import subprocess
import json
import xml.dom.minidom as xdm
from relalign import perform_relative_alignment


def write_tv_calibration_to_file(file_name, camera_matrix, dist_coeffs, tv_width, tv_height):
    doc = xdm.Document()
    base = doc.createElement('calibration')
    doc.appendChild(base)

    entry_names = ('projection', 'width', 'height', 'fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'k3', 'p1', 'p2')
    entry_values = ('frame', tv_width, tv_height, camera_matrix[0,0],
                    camera_matrix[1,1], camera_matrix[0,2], camera_matrix[1,2],
                    dist_coeffs[0], dist_coeffs[1], dist_coeffs[2], 0, 0)

    for name, value in zip(entry_names, entry_values):
        entry = doc.createElement(name)
        base.appendChild(entry)
        entry.appendChild(doc.createTextNode(str(value)))

    doc.writexml(open(file_name, 'w'),
           indent="  ",
           encoding="utf-8")


def read_matrices(file_name):
    f = open(file_name, "r")
    data = []
    for s in f:
        lst = json.loads(s)
        data.append(lst)

    print('camera_matrix_rgb:')
    print(ps.Matrix(data[0]))
    print('dist_coefs_rgb:')
    print([float(x) for x in data[1]])

    tv_to_rgb_matrix = ps.Matrix(data[4])
    cameraMatrix_tv = ps.Matrix(data[2])
    distCoeffs_tv = [float(x) for x in data[3]]
    image_size = list(data[5])

    return tv_to_rgb_matrix, cameraMatrix_tv, distCoeffs_tv, image_size[0], image_size[1]

def show_all_widgets_in_layout(layout, show):
    items = (layout.itemAt(i) for i in range(layout.count())) 
    for item in items:
        if item.widget() is not None:
            item.widget().hide()
        if item.layout():
            show_all_widgets_in_layout(item.layout(), show)


class ControlDialog(QtGui.QDialog):
    MIN_CALIBRATION_FILES = 1
    PHOTO_CORRESPONDENCE = 2
    CALIBRATION_CORRESPONDENCE = 1
    WHEN_CAN_START = CALIBRATION_CORRESPONDENCE | PHOTO_CORRESPONDENCE

    DEFAULT_LOCATION = "/home/plaz/Thermal_vision/samples/rgb"
    DEFAULT_MATRICES_FILE = temp_directory + os.sep + 'calib_data.txt'

    def __init__(self, parent=None):
        super(ControlDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
       
        self.ui.groupBox_3.setEnabled(False)
        self.ui.cell_size_edit.setValidator(QtGui.QDoubleValidator(0, 100, 4, self))

        self.setFixedSize(self.size())
        self.initial_width = self.width()
        self.initial_height = self.height()
        self.calculate_matrices_height = self.ui.groupBox_2.height()
        self.clear()

    def clear_calculate_matrices_data(self):
        self.ui.rgb_photos_ok_checkbox.setChecked(False)
        self.ui.tv_photos_ok_checkbox.setChecked(False)
        self.rgb_checkboxes = []
        self.tv_comboboxes = []
        self.tv_calibration_files = None
        self.rgb_calibration_files = None
        self.rgb_short_file_names = None
        self.tv_short_file_names = None
        self.checked_correpsonfing_photos = 0
        self.ui.rgb_tv_table.clearContents()
        self.ui.rgb_tv_table.setRowCount(0)
        self.ui.cell_size_edit.setText("0.1")
        self.file_name_to_save_matrices = ControlDialog.DEFAULT_MATRICES_FILE
        self.ui.save_matrices_file_edit.setText("")
        self.can_start_flag &= ~ControlDialog.CALIBRATION_CORRESPONDENCE

    def clear_load_matrices_data(self):
        self.file_name_to_load_matrices = None
        self.ui.select_matrices_file_edit.setText("")
        self.can_start_flag &= ~ControlDialog.CALIBRATION_CORRESPONDENCE

    def clear(self):
        self.can_start_flag = 0
        self.clear_calculate_matrices_data()
        self.clear_load_matrices_data()

        self.can_start_flag = 0
        self.ui.matching_file_edit.setText("")
        self.ui.ok_button.setEnabled(False)
        self.photo_matching_file = None
        self.ui.matching_file_edit.setText("")
        self.want_calculate = True
        pass

    def perform_calibration(self):
        rgb_images = self.rgb_calibration_files
        tv_images = self.tv_calibration_files
        
        rgb_relative_file_names = []
        tv_relative_file_names = []
        for i, chbox in enumerate(self.rgb_checkboxes):
            if not chbox.isChecked():
                continue
            rgb_relative_file_names.append(self.rgb_calibration_files[i])
            tv_relative_file_names.append(self.tv_calibration_files[self.tv_comboboxes[i].currentIndex()])

        cell_size = float(self.ui.cell_size_edit.text())

        config_abs_path = self.write_config(rgb_images, tv_images, rgb_relative_file_names, tv_relative_file_names, cell_size)

        commandline_args = ["--config", config_abs_path]
        commandline_args += ["--save-file", self.file_name_to_save_matrices]

        print(commandline_args)
        #with open('query.txt','w') as stdout:
        p = subprocess.call([support_directory + os.sep + "run_calibration.sh"] + commandline_args)

        '''while True:
            print('here')
            output = p.stdout.readline()
            if output == '' and p.poll() is not None:
                break
            if output:
                print (output.strip())

            rc = p.poll()'''

        msgBox = QtGui.QMessageBox()
        msgBox.setText("Succesfully calibrated cameras.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.show()

    def ok_pressed(self):
        cur_dir = os.getcwd()
        os.chdir(temp_directory)  

        if self.want_calculate:
            self.perform_calibration()
            self.file_name_to_load_matrices = self.file_name_to_save_matrices

        tv_to_rgb_matrix, cameraMatrix_tv, distCoeffs_tv, tv_image_width, \
            tv_image_height = read_matrices(self.file_name_to_save_matrices)

        calibration_file_name = temp_directory + os.sep + 'tv_calibration.txt'
        write_tv_calibration_to_file(calibration_file_name, cameraMatrix_tv, distCoeffs_tv, tv_image_width, tv_image_height)

        os.chdir(cur_dir)  

        perform_relative_alignment(tv_to_rgb_matrix, self.photo_matching_file, calibration_file_name) #uncomment
        
        self.clear()
        self.hide()

    def write_config(self, rgb_images, tv_images, rgb_relative_file_names, tv_relative_file_names, cell_size):
        config_file_name = 'config.txt'
        abs_path = os.path.abspath(config_file_name)
        f = open(config_file_name, "w")
        f.write(str(len(rgb_images)) + '\n')
        for name in rgb_images:
            f.write(name + '\n')

        f.write(str(len(tv_images)) + '\n')
        for name in tv_images:
            f.write(name + '\n')
        f.write(str(cell_size) + '\n')

        f.write(str(len(rgb_relative_file_names)) + '\n')
        for r, t in zip(rgb_relative_file_names, tv_relative_file_names):
            f.write(r + '\n')
            f.write(t + '\n')
        f.close()
        return abs_path


    def save_matrices_to_file_clicked(self):
        options = QtGui.QFileDialog.Options()

        file_name, filtr = QtGui.QFileDialog.getSaveFileName(self,
                "QFileDialog.getSaveFileName()",
                "calibration.txt",
                "All Files (*);;Text Files (*.txt)", "", options)
        if file_name is not None:
            self.file_name_to_save_matrices = file_name
            self.ui.save_matrices_file_edit.setText(file_name)
        else:
            self.file_name_to_save_matrices = ControlDialog.DEFAULT_MATRICES_FILE


    def use_matrices_from_file_clicked(self):
        file_name = self.select_text_file_clicked()
        if file_name is None:
            return
        self.file_name_to_load_matrices = file_name
        self.ui.select_matrices_file_edit.setText(file_name)
        self.can_start_flag |= ControlDialog.CALIBRATION_CORRESPONDENCE

    def calculate_matrices_radio_clicked(self):
        self.ui.groupBox_2.setEnabled(True)
        self.ui.groupBox_3.setEnabled(False)
        self.clear_load_matrices_data()
        self.want_calculate = True

    def select_matrices_radio_clicked(self):
        self.ui.groupBox_3.setEnabled(True)
        self.ui.groupBox_2.setEnabled(False)
        self.clear_calculate_matrices_data()
        self.want_calculate = False

    def select_calibration_files_clicked(self):
        files = QtGui.QFileDialog.getOpenFileNames(
                        self,
                        "Select one or more files to open",
                        ControlDialog.DEFAULT_LOCATION,
                        "Images (*.png *.xpm *.jpg *.bmp)")[0];
        if len(files) >= ControlDialog.MIN_CALIBRATION_FILES:
            return files
        else:
            ret = QtGui.QMessageBox.information(self, self.tr("Calibration files"),
                   self.tr("Not enough files for calibration. Should be at least " + str(ControlDialog.MIN_CALIBRATION_FILES)),
                   QtGui.QMessageBox.Ok)

            return None

    def select_text_file_clicked(self):
        file_name = QtGui.QFileDialog.getOpenFileName(
                        self,
                        "Select file to open",
                        ControlDialog.DEFAULT_LOCATION,
                        "Text files (*.txt)")[0];
        return file_name

    def update_tv_comboboxes(self):
        for i, cbox in enumerate(self.tv_comboboxes):
            cbox.clear()
            cbox.addItems(self.tv_short_file_names)
            self.rgb_checkboxes[i].stateChanged.connect(cbox.setEnabled)
            self.rgb_checkboxes[i].setEnabled(True)
            

    def select_rgb_calib_files_clicked(self):
        files = self.select_calibration_files_clicked()
        if files is not None:
            self.checked_correpsonfing_photos = 0
            self.rgb_calibration_files = files
            self.ui.rgb_photos_ok_checkbox.setChecked(True)
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
            self.ui.tv_photos_ok_checkbox.setChecked(True)
            self.update_tv_comboboxes()

        self.ui.ok_button.setEnabled(self.can_start_flag == ControlDialog.WHEN_CAN_START)

    def table_checkbox_clicked(self, checked):
        if checked and self.tv_calibration_files:
            self.can_start_flag |= ControlDialog.CALIBRATION_CORRESPONDENCE
            self.checked_correpsonfing_photos += 1
        else:
            self.checked_correpsonfing_photos -= 1
            if self.checked_correpsonfing_photos == 0:
                self.can_start_flag &= (~ControlDialog.CALIBRATION_CORRESPONDENCE)
        
        self.ui.ok_button.setEnabled(self.can_start_flag == ControlDialog.WHEN_CAN_START)

    def on_select_matching_file_button_clicked(self):
        self.photo_matching_file = self.select_text_file_clicked()
        if self.photo_matching_file:
            self.can_start_flag |= ControlDialog.PHOTO_CORRESPONDENCE
            self.ui.matching_file_edit.setText(self.photo_matching_file)
        else:
            self.can_start_flag &= (~ControlDialog.PHOTO_CORRESPONDENCE)
            self.ui.matching_file_edit.setText("")
        self.ui.ok_button.setEnabled(self.can_start_flag == ControlDialog.WHEN_CAN_START)

    def match_photos_by_file_radio_clicked(self):
        if self.photo_matching_file:
            self.can_start_flag |= ControlDialog.PHOTO_CORRESPONDENCE
        else:
            self.can_start_flag &= (~ControlDialog.PHOTO_CORRESPONDENCE)
        self.ui.matching_file_edit.setEnabled(True)
        self.ui.matching_file_button.setEnabled(True)
        self.ui.ok_button.setEnabled(self.can_start_flag == ControlDialog.WHEN_CAN_START)

    def match_photos_by_location_radio_clicked(self):
        self.can_start_flag |= ControlDialog.PHOTO_CORRESPONDENCE
        self.ui.matching_file_edit.setEnabled(False)
        self.ui.matching_file_button.setEnabled(False)

        self.ui.ok_button.setEnabled(self.can_start_flag == ControlDialog.WHEN_CAN_START)


def f():
    dlg.show()


def main():
    qtapp = QtGui.QApplication(sys.argv)
    dlg = ControlDialog()
    dlg.show()
    qtapp.exec_()

DEBUG = False

if DEBUG:
    if __name__ == '__main__':
        main()
else:
    dlg = ControlDialog()
    ps.app.addMenuItem("Workflow/Relative Photo Alignment...", f) #uncomment

#/usr/bin/python

import sys
import os
import time

encoding = 'utf8'
if sys.getfilesystemencoding() == 'mbcs':
    encoding = 'cp1251'

support_directory = os.path.dirname(
    os.path.realpath(__file__)) + os.sep + u'support'
support_directory = str(
    support_directory.encode(sys.getfilesystemencoding()), 'utf8')
temp_directory = support_directory + os.sep + '.tmp'
sys.path.append(support_directory)

from PySide import QtCore, QtGui
from dialog_ui import Ui_Dialog
import PhotoScan as ps
import subprocess
import json
import xml.dom.minidom as xdm
from relalign import perform_relative_alignment
import camera_relative_position as crp
from functools import partial

import numpy as np
import cv2


def check_can_write_file(file_name):
    try:
        f = open(file_name, "w")
        return True
    except OSError:
        return False


def has_numpy_and_cv():
    has_numpy = 'sqrt' in dir(np)
    has_cv = 'stereoCalibrate' in dir(cv2)
    return has_cv and has_numpy


def write_tv_calibration_to_file(file_name, camera_matrix, dist_coeffs, tv_width, tv_height):
    doc = xdm.Document()
    base = doc.createElement('calibration')
    doc.appendChild(base)

    entry_names = ('projection', 'width', 'height',
                   'fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'k3', 'p1', 'p2')
    entry_values = ('frame', tv_width, tv_height, camera_matrix[0, 0],
                    camera_matrix[1, 1], camera_matrix[
                        0, 2], camera_matrix[1, 2],
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
        self.ui.cell_size_edit.setValidator(
            QtGui.QDoubleValidator(0, 100, 4, self))

        self.setFixedSize(self.size())
        self.initial_width = self.width()
        self.initial_height = self.height()
        self.calculate_matrices_height = self.ui.groupBox_2.height()
        self.last_path = ControlDialog.DEFAULT_LOCATION
        self.translator = None

        self.progress = QtGui.QProgressDialog(
            self.tr("Calibrating images..."), self.tr("Cancel"), 0, 100, self)
        self.progress.setWindowTitle('Calibration progress')
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.canceled.connect(self.calibration_canceled)
        self.progress.resize(self.progress.sizeHint() + QtCore.QSize(30, 0))
        self.worker = crp.CalibratorThread()
        self.worker.update_progress.connect(self.set_progress)
        self.clear()

    def calibration_canceled(self):
        self.worker.terminate()
        print('Calibration canceled')
        while not self.worker.isFinished():
            time.sleep(0.1)

    def show(self):
        super(ControlDialog, self).show()
        self.clear()

    def set_progress(self, progress):
        self.progress.setValue(progress)

    def set_translator(self, translator):
        self.translator = translator

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
        self.progress.hide()

    def perform_calibration(self):
        rgb_images = self.rgb_calibration_files
        tv_images = self.tv_calibration_files

        rgb_relative_file_names = []
        tv_relative_file_names = []
        for i, chbox in enumerate(self.rgb_checkboxes):
            if not chbox.isChecked():
                continue
            rgb_relative_file_names.append(self.rgb_calibration_files[i])
            tv_relative_file_names.append(
                self.tv_calibration_files[self.tv_comboboxes[i].currentIndex()])

        cell_size = float(self.ui.cell_size_edit.text())

        config_abs_path = self.write_config(
            rgb_images, tv_images, rgb_relative_file_names, tv_relative_file_names, cell_size)

        save_file = str(self.file_name_to_save_matrices.encode(
            sys.getfilesystemencoding()), encoding)

        if not has_numpy_and_cv():
            commandline_args = ["--config", config_abs_path]
            commandline_args += ["--save-file", save_file]
            if os.name != 'nt':
                p = subprocess.call(
                    [support_directory + os.sep + "run_calibration.sh"] + commandline_args)
            else:
                pass  # TODO write bat file
            return False
        else:  # windows
            self.worker.reset(config_abs_path, save_file)
            self.set_progress(0)
            self.worker.start()
            self.progress.show()
            while self.worker.isRunning():
                QtGui.qApp.processEvents()
                time.sleep(0.1)
            self.progress.hide()
            return self.progress.wasCanceled()

    def ok_pressed(self):
        cur_dir = os.getcwd()
        os.chdir(temp_directory)

        if self.want_calculate:
            has_embedded_cv_and_numpy = self.perform_calibration()
            self.file_name_to_load_matrices = str(self.file_name_to_save_matrices.encode(
                sys.getfilesystemencoding()), encoding)
            if has_embedded_cv_and_numpy:
                self.progress.reset()
                os.chdir(cur_dir)
                return

        try:
            tv_to_rgb_matrix, cameraMatrix_tv, distCoeffs_tv, tv_image_width, \
                tv_image_height = read_matrices(
                    self.file_name_to_load_matrices)
        except:
            print(
                "Error loading calibrations file. Make sure file was produced with this software.")
            os.chdir(cur_dir)
            return

        calibration_file_name = temp_directory + os.sep + 'tv_calibration.txt'
        write_tv_calibration_to_file(
            calibration_file_name, cameraMatrix_tv, distCoeffs_tv, tv_image_width, tv_image_height)

        os.chdir(cur_dir)

        perform_relative_alignment(
            tv_to_rgb_matrix, self.photo_matching_file, calibration_file_name)  # uncomment
        msgBox = QtGui.QMessageBox()
        print('Relative alignment finished')
        msgBox.setText("Succesfully calibrated cameras.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.buttonClicked.connect(self.hide)
        msgBox.exec()

    def write_config(self, rgb_images, tv_images, rgb_relative_file_names, tv_relative_file_names, cell_size):
        config_file_name = 'config.txt'
        abs_path = os.path.abspath(config_file_name)
        abs_path = str(abs_path.encode(sys.getfilesystemencoding()), encoding)

        f = open(config_file_name, "w")
        f.write(str(len(rgb_images)) + '\n')
        for name in rgb_images:
            n = str(name.encode(sys.getfilesystemencoding()), encoding)
            f.write(n + '\n')

        f.write(str(len(tv_images)) + '\n')
        for name in tv_images:
            n = str(name.encode(sys.getfilesystemencoding()), encoding)
            f.write(n + '\n')
        f.write(str(cell_size) + '\n')

        f.write(str(len(rgb_relative_file_names)) + '\n')
        for r, t in zip(rgb_relative_file_names, tv_relative_file_names):
            rgb = str(r.encode(sys.getfilesystemencoding()), encoding)
            tv = str(t.encode(sys.getfilesystemencoding()), encoding)
            f.write(rgb + '\n')
            f.write(tv + '\n')
        f.close()
        return abs_path

    # def tr(self, str):
    #    return self.translator.translate('dlg', str)

    def save_matrices_to_file_clicked(self):
        options = QtGui.QFileDialog.Options()

        file_name, filtr = QtGui.QFileDialog.getSaveFileName(self,
                                                             "QFileDialog.getSaveFileName()",
                                                             self.last_path + os.sep +
                                                             "calibration.txt",
                                                             "All Files (*);;Text Files (*.txt)", "", options)
        if file_name is not None and check_can_write_file(file_name):

            self.file_name_to_save_matrices = file_name
            self.ui.save_matrices_file_edit.setText(file_name)
        else:
            self.file_name_to_save_matrices = ControlDialog.DEFAULT_MATRICES_FILE

            self.ui.save_matrices_file_edit.setText("")

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
            self.last_path,
            "Images (*.png *.xpm *.jpg *.bmp)")[0]

        if files is not None and len(files) > 0:
            self.last_path = os.path.dirname(files[0])
        if len(files) >= ControlDialog.MIN_CALIBRATION_FILES:
            return files
        else:
            ret = QtGui.QMessageBox.information(
                self, self.tr("Calibration files"),
                self.tr("Not enough files for calibration. Should be at least " + str(
                        ControlDialog.MIN_CALIBRATION_FILES)),
                QtGui.QMessageBox.Ok)

            return None

    def select_text_file_clicked(self):
        file_name = QtGui.QFileDialog.getOpenFileName(
            self,
            "Select file to open",
            self.last_path,
            "Text files (*.txt)")[0]
        if file_name is not None:
            self.last_path = os.path.dirname(file_name)
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
            self.rgb_short_file_names = [s.split(os.sep)[-1] for s in files]

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
                self.ui.rgb_tv_table.setCellWidget(i, 0, new_check_box)

                new_combo_box = QtGui.QComboBox(self)
                self.tv_comboboxes.append(new_combo_box)
                self.ui.rgb_tv_table.setCellWidget(i, 1, new_combo_box)
                new_combo_box.setEnabled(False)

            if self.tv_calibration_files:
                self.update_tv_comboboxes()

    def select_tv_calib_files_clicked(self):
        files = self.select_calibration_files_clicked()
        if files is not None:
            self.tv_short_file_names = [s.split(os.sep)[-1] for s in files]
            self.tv_calibration_files = files
            self.ui.tv_photos_ok_checkbox.setChecked(True)
            self.update_tv_comboboxes()

        self.ui.ok_button.setEnabled(
            self.can_start_flag == ControlDialog.WHEN_CAN_START)

    def table_checkbox_clicked(self, checked):
        if checked and self.tv_calibration_files:
            self.can_start_flag |= ControlDialog.CALIBRATION_CORRESPONDENCE
            self.checked_correpsonfing_photos += 1
        else:
            self.checked_correpsonfing_photos -= 1
            if self.checked_correpsonfing_photos == 0:
                self.can_start_flag &= (
                    ~ControlDialog.CALIBRATION_CORRESPONDENCE)

        self.ui.ok_button.setEnabled(
            self.can_start_flag == ControlDialog.WHEN_CAN_START)

    def on_select_matching_file_button_clicked(self):
        self.photo_matching_file = self.select_text_file_clicked()
        if self.photo_matching_file:
            self.can_start_flag |= ControlDialog.PHOTO_CORRESPONDENCE
            self.ui.matching_file_edit.setText(self.photo_matching_file)
        else:
            self.can_start_flag &= (~ControlDialog.PHOTO_CORRESPONDENCE)
            self.ui.matching_file_edit.setText("")
        self.ui.ok_button.setEnabled(
            self.can_start_flag == ControlDialog.WHEN_CAN_START)

    def match_photos_by_file_radio_clicked(self):
        if self.photo_matching_file:
            self.can_start_flag |= ControlDialog.PHOTO_CORRESPONDENCE
        else:
            self.can_start_flag &= (~ControlDialog.PHOTO_CORRESPONDENCE)
        self.ui.matching_file_edit.setEnabled(True)
        self.ui.matching_file_button.setEnabled(True)
        self.ui.ok_button.setEnabled(
            self.can_start_flag == ControlDialog.WHEN_CAN_START)

    def match_photos_by_location_radio_clicked(self):
        self.can_start_flag |= ControlDialog.PHOTO_CORRESPONDENCE
        self.ui.matching_file_edit.setEnabled(False)
        self.ui.matching_file_button.setEnabled(False)

        self.ui.ok_button.setEnabled(
            self.can_start_flag == ControlDialog.WHEN_CAN_START)


def f():
    dlg.show()


def set_translator(qtapp):
    settings = QtCore.QSettings()
    lang = settings.value('main/language')
    translator = QtCore.QTranslator()

    trans_file = 'en_GB'
    if lang == 'ru':
        trans_file = 'ru_RU'

    translator.load(support_directory + os.sep + 'trans' + os.sep + trans_file)
    qtapp.installTranslator(translator)
    return translator


def main():
    qtapp = QtGui.QApplication(sys.argv)
    set_translator(qtapp)

    mw = None
    for widget in qtapp.topLevelWidgets():
        if type(widget) is QtGui.QMainWidget:
            mw = widget

    print(mw)
    dlg = ControlDialog(qtapp)
    dlg.show()
    qtapp.exec_()

DEBUG = False

if DEBUG:
    if __name__ == '__main__':
        main()
else:
    qtapp = QtGui.QApplication.instance()

    mw = None
    for widget in qtapp.topLevelWidgets():
        if type(widget) is QtGui.QMainWindow:
            mw = widget
            print(mw)
    dlg = ControlDialog(mw)
    translator = set_translator(qtapp)
    dlg.set_translator(translator)
    ps.app.addMenuItem(
        dlg.tr("Workflow/Relative Photo Alignment..."), f)  # uncomment

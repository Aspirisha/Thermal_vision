# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Mon Nov  9 19:20:19 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(478, 703)
        self.ok_button = QtGui.QPushButton(Dialog)
        self.ok_button.setEnabled(False)
        self.ok_button.setGeometry(QtCore.QRect(80, 670, 99, 27))
        self.ok_button.setObjectName("ok_button")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 441, 161))
        self.groupBox.setObjectName("groupBox")
        self.radio_by_distance_4 = QtGui.QRadioButton(self.groupBox)
        self.radio_by_distance_4.setGeometry(QtCore.QRect(30, 20, 117, 22))
        self.radio_by_distance_4.setChecked(True)
        self.radio_by_distance_4.setObjectName("radio_by_distance_4")
        self.radio_by_name_4 = QtGui.QRadioButton(self.groupBox)
        self.radio_by_name_4.setGeometry(QtCore.QRect(30, 40, 117, 22))
        self.radio_by_name_4.setObjectName("radio_by_name_4")
        self.gridLayoutWidget_4 = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(0, 70, 441, 85))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.by_name_options_layout_4 = QtGui.QGridLayout(self.gridLayoutWidget_4)
        self.by_name_options_layout_4.setContentsMargins(0, 0, 0, 0)
        self.by_name_options_layout_4.setObjectName("by_name_options_layout_4")
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.rgb_index_label_4 = QtGui.QLabel(self.gridLayoutWidget_4)
        self.rgb_index_label_4.setObjectName("rgb_index_label_4")
        self.horizontalLayout_16.addWidget(self.rgb_index_label_4)
        self.rgb_prefix_edit_4 = QtGui.QLineEdit(self.gridLayoutWidget_4)
        self.rgb_prefix_edit_4.setObjectName("rgb_prefix_edit_4")
        self.horizontalLayout_16.addWidget(self.rgb_prefix_edit_4)
        self.rgb_prefix_label_4 = QtGui.QLabel(self.gridLayoutWidget_4)
        self.rgb_prefix_label_4.setObjectName("rgb_prefix_label_4")
        self.horizontalLayout_16.addWidget(self.rgb_prefix_label_4)
        self.rgb_index_edit_4 = QtGui.QLineEdit(self.gridLayoutWidget_4)
        self.rgb_index_edit_4.setObjectName("rgb_index_edit_4")
        self.horizontalLayout_16.addWidget(self.rgb_index_edit_4)
        self.by_name_options_layout_4.addLayout(self.horizontalLayout_16, 1, 0, 1, 1)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.tv_index_label_4 = QtGui.QLabel(self.gridLayoutWidget_4)
        self.tv_index_label_4.setObjectName("tv_index_label_4")
        self.horizontalLayout_17.addWidget(self.tv_index_label_4)
        self.tv_prefix_edit_4 = QtGui.QLineEdit(self.gridLayoutWidget_4)
        self.tv_prefix_edit_4.setObjectName("tv_prefix_edit_4")
        self.horizontalLayout_17.addWidget(self.tv_prefix_edit_4)
        self.tv_prefix_label_4 = QtGui.QLabel(self.gridLayoutWidget_4)
        self.tv_prefix_label_4.setObjectName("tv_prefix_label_4")
        self.horizontalLayout_17.addWidget(self.tv_prefix_label_4)
        self.tv_index_edit_4 = QtGui.QLineEdit(self.gridLayoutWidget_4)
        self.tv_index_edit_4.setObjectName("tv_index_edit_4")
        self.horizontalLayout_17.addWidget(self.tv_index_edit_4)
        self.by_name_options_layout_4.addLayout(self.horizontalLayout_17, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 200, 461, 461))
        self.groupBox_2.setObjectName("groupBox_2")
        self.radio_calculate_matrices_4 = QtGui.QRadioButton(self.groupBox_2)
        self.radio_calculate_matrices_4.setGeometry(QtCore.QRect(30, 30, 181, 22))
        self.radio_calculate_matrices_4.setObjectName("radio_calculate_matrices_4")
        self.verticalLayoutWidget_4 = QtGui.QWidget(self.groupBox_2)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 60, 431, 321))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.calculate_matrices_opt_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget_4)
        self.calculate_matrices_opt_layout.setContentsMargins(0, 0, 0, 0)
        self.calculate_matrices_opt_layout.setObjectName("calculate_matrices_opt_layout")
        self.horizontalLayout_18 = QtGui.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.tv_calibration_files_button_4 = QtGui.QPushButton(self.verticalLayoutWidget_4)
        self.tv_calibration_files_button_4.setObjectName("tv_calibration_files_button_4")
        self.horizontalLayout_18.addWidget(self.tv_calibration_files_button_4)
        self.tv_calibration_files_edit_4 = QtGui.QLineEdit(self.verticalLayoutWidget_4)
        self.tv_calibration_files_edit_4.setObjectName("tv_calibration_files_edit_4")
        self.horizontalLayout_18.addWidget(self.tv_calibration_files_edit_4)
        self.calculate_matrices_opt_layout.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19 = QtGui.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.rgb_calibration_files_button_4 = QtGui.QPushButton(self.verticalLayoutWidget_4)
        self.rgb_calibration_files_button_4.setObjectName("rgb_calibration_files_button_4")
        self.horizontalLayout_19.addWidget(self.rgb_calibration_files_button_4)
        self.rgb_calibration_files_edit_4 = QtGui.QLineEdit(self.verticalLayoutWidget_4)
        self.rgb_calibration_files_edit_4.setObjectName("rgb_calibration_files_edit_4")
        self.horizontalLayout_19.addWidget(self.rgb_calibration_files_edit_4)
        self.calculate_matrices_opt_layout.addLayout(self.horizontalLayout_19)
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget_4)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.calculate_matrices_opt_layout.addWidget(self.label_5)
        self.rgb_tv_table = QtGui.QTableWidget(self.verticalLayoutWidget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rgb_tv_table.sizePolicy().hasHeightForWidth())
        self.rgb_tv_table.setSizePolicy(sizePolicy)
        self.rgb_tv_table.setRowCount(1)
        self.rgb_tv_table.setObjectName("rgb_tv_table")
        self.rgb_tv_table.setColumnCount(2)
        self.rgb_tv_table.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.rgb_tv_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.rgb_tv_table.setHorizontalHeaderItem(1, item)
        self.rgb_tv_table.horizontalHeader().setCascadingSectionResizes(True)
        self.rgb_tv_table.horizontalHeader().setDefaultSectionSize(200)
        self.rgb_tv_table.horizontalHeader().setMinimumSectionSize(200)
        self.rgb_tv_table.horizontalHeader().setStretchLastSection(True)
        self.calculate_matrices_opt_layout.addWidget(self.rgb_tv_table)
        self.horizontalLayoutWidget_6 = QtGui.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(0, 420, 431, 41))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.calibration_file_options_layout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.calibration_file_options_layout.setContentsMargins(0, 0, 0, 0)
        self.calibration_file_options_layout.setObjectName("calibration_file_options_layout")
        self.select_calibration_file_button = QtGui.QPushButton(self.horizontalLayoutWidget_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_calibration_file_button.sizePolicy().hasHeightForWidth())
        self.select_calibration_file_button.setSizePolicy(sizePolicy)
        self.select_calibration_file_button.setObjectName("select_calibration_file_button")
        self.calibration_file_options_layout.addWidget(self.select_calibration_file_button)
        self.select_calibration_file_edit = QtGui.QLineEdit(self.horizontalLayoutWidget_6)
        self.select_calibration_file_edit.setObjectName("select_calibration_file_edit")
        self.calibration_file_options_layout.addWidget(self.select_calibration_file_edit)
        self.radio_use_file_matrices_4 = QtGui.QRadioButton(self.groupBox_2)
        self.radio_use_file_matrices_4.setGeometry(QtCore.QRect(30, 390, 261, 22))
        self.radio_use_file_matrices_4.setObjectName("radio_use_file_matrices_4")
        self.cancel_button = QtGui.QPushButton(Dialog)
        self.cancel_button.setEnabled(True)
        self.cancel_button.setGeometry(QtCore.QRect(250, 670, 99, 27))
        self.cancel_button.setObjectName("cancel_button")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Thermal texturing", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_button.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Select thermal and rgb photos matching", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_by_distance_4.setText(QtGui.QApplication.translate("Dialog", "By distance", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_by_name_4.setText(QtGui.QApplication.translate("Dialog", "By name", None, QtGui.QApplication.UnicodeUTF8))
        self.rgb_index_label_4.setText(QtGui.QApplication.translate("Dialog", "TV prefix:", None, QtGui.QApplication.UnicodeUTF8))
        self.rgb_prefix_label_4.setText(QtGui.QApplication.translate("Dialog", "TV index:", None, QtGui.QApplication.UnicodeUTF8))
        self.tv_index_label_4.setText(QtGui.QApplication.translate("Dialog", "RGB prefix:", None, QtGui.QApplication.UnicodeUTF8))
        self.tv_prefix_label_4.setText(QtGui.QApplication.translate("Dialog", "RGB index:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Calibration setup", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_calculate_matrices_4.setText(QtGui.QApplication.translate("Dialog", "Calculate matrices", None, QtGui.QApplication.UnicodeUTF8))
        self.tv_calibration_files_button_4.setText(QtGui.QApplication.translate("Dialog", "Select TV calibration files", None, QtGui.QApplication.UnicodeUTF8))
        self.rgb_calibration_files_button_4.setText(QtGui.QApplication.translate("Dialog", "Select RGB calibration files", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Corresponding TV and RGB photos:", None, QtGui.QApplication.UnicodeUTF8))
        self.rgb_tv_table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Dialog", "RGB photo", None, QtGui.QApplication.UnicodeUTF8))
        self.rgb_tv_table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "TV photo", None, QtGui.QApplication.UnicodeUTF8))
        self.select_calibration_file_button.setText(QtGui.QApplication.translate("Dialog", "Select file", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_use_file_matrices_4.setText(QtGui.QApplication.translate("Dialog", "Use calibration matrices from file", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

class ControlDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ControlDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

qtapp = QtGui.QApplication(sys.argv)
dlg = ControlDialog()
dlg.show()
qtapp.exec_()
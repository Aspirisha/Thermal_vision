# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Fri Dec 18 18:07:59 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 693)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(50, 620, 341, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ok_button = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.ok_button.setEnabled(False)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout_3.addWidget(self.ok_button)
        self.cancel_button = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.cancel_button.setEnabled(True)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_3.addWidget(self.cancel_button)
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_5.setGeometry(QtCore.QRect(0, 0, 471, 471))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 471))
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.radio_calculate_matrices = QtGui.QRadioButton(self.groupBox_5)
        self.radio_calculate_matrices.setGeometry(QtCore.QRect(0, 10, 181, 22))
        self.radio_calculate_matrices.setChecked(True)
        self.radio_calculate_matrices.setObjectName("radio_calculate_matrices")
        self.radio_use_file_matrices = QtGui.QRadioButton(self.groupBox_5)
        self.radio_use_file_matrices.setGeometry(QtCore.QRect(0, 40, 261, 22))
        self.radio_use_file_matrices.setObjectName("radio_use_file_matrices")
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox_5)
        self.groupBox_2.setGeometry(QtCore.QRect(-20, 60, 451, 401))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget = QtGui.QWidget(self.groupBox_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 431, 391))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.calculate_matrices_opt_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.calculate_matrices_opt_layout.setContentsMargins(5, -1, 5, -1)
        self.calculate_matrices_opt_layout.setObjectName("calculate_matrices_opt_layout")
        self.horizontalLayout8 = QtGui.QHBoxLayout()
        self.horizontalLayout8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout8.setObjectName("horizontalLayout8")
        self.calculate_matrices_opt_layout.addLayout(self.horizontalLayout8)
        self.formLayout_6 = QtGui.QFormLayout()
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setContentsMargins(0, -1, 0, -1)
        self.formLayout_6.setObjectName("formLayout_6")
        self.rgb_calibration_files_button = QtGui.QPushButton(self.verticalLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 208, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(182, 255, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(155, 231, 53))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 104, 11))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 139, 14))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 208, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(191, 231, 138))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 208, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(182, 255, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(155, 231, 53))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 104, 11))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 139, 14))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 208, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(191, 231, 138))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 104, 11))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 208, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(182, 255, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(155, 231, 53))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 104, 11))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 139, 14))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 104, 11))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 104, 11))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 208, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 208, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 208, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.rgb_calibration_files_button.setPalette(palette)
        self.rgb_calibration_files_button.setObjectName("rgb_calibration_files_button")
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.rgb_calibration_files_button)
        self.tv_photos_ok_checkbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.tv_photos_ok_checkbox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tv_photos_ok_checkbox.sizePolicy().hasHeightForWidth())
        self.tv_photos_ok_checkbox.setSizePolicy(sizePolicy)
        self.tv_photos_ok_checkbox.setText("")
        self.tv_photos_ok_checkbox.setCheckable(True)
        self.tv_photos_ok_checkbox.setChecked(False)
        self.tv_photos_ok_checkbox.setAutoRepeat(False)
        self.tv_photos_ok_checkbox.setObjectName("tv_photos_ok_checkbox")
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.LabelRole, self.tv_photos_ok_checkbox)
        self.tv_calibration_files_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.tv_calibration_files_button.setObjectName("tv_calibration_files_button")
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.FieldRole, self.tv_calibration_files_button)
        self.rgb_photos_ok_checkbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.rgb_photos_ok_checkbox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rgb_photos_ok_checkbox.sizePolicy().hasHeightForWidth())
        self.rgb_photos_ok_checkbox.setSizePolicy(sizePolicy)
        self.rgb_photos_ok_checkbox.setText("")
        self.rgb_photos_ok_checkbox.setCheckable(True)
        self.rgb_photos_ok_checkbox.setChecked(False)
        self.rgb_photos_ok_checkbox.setAutoRepeat(False)
        self.rgb_photos_ok_checkbox.setObjectName("rgb_photos_ok_checkbox")
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.rgb_photos_ok_checkbox)
        self.calculate_matrices_opt_layout.addLayout(self.formLayout_6)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cell_size_edit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.cell_size_edit.setObjectName("cell_size_edit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cell_size_edit)
        self.calculate_matrices_opt_layout.addLayout(self.formLayout)
        self.rgb_tv_table = QtGui.QTableWidget(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rgb_tv_table.sizePolicy().hasHeightForWidth())
        self.rgb_tv_table.setSizePolicy(sizePolicy)
        self.rgb_tv_table.setRowCount(0)
        self.rgb_tv_table.setObjectName("rgb_tv_table")
        self.rgb_tv_table.setColumnCount(2)
        self.rgb_tv_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.rgb_tv_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.rgb_tv_table.setHorizontalHeaderItem(1, item)
        self.rgb_tv_table.horizontalHeader().setCascadingSectionResizes(True)
        self.rgb_tv_table.horizontalHeader().setDefaultSectionSize(200)
        self.rgb_tv_table.horizontalHeader().setMinimumSectionSize(200)
        self.rgb_tv_table.horizontalHeader().setStretchLastSection(True)
        self.calculate_matrices_opt_layout.addWidget(self.rgb_tv_table)
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.calculate_matrices_opt_layout.addWidget(self.label)
        self.calibration_file_options_layout_3 = QtGui.QHBoxLayout()
        self.calibration_file_options_layout_3.setObjectName("calibration_file_options_layout_3")
        self.matrices_save_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.matrices_save_button.setObjectName("matrices_save_button")
        self.calibration_file_options_layout_3.addWidget(self.matrices_save_button)
        self.save_matrices_file_edit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.save_matrices_file_edit.setText("")
        self.save_matrices_file_edit.setReadOnly(True)
        self.save_matrices_file_edit.setObjectName("save_matrices_file_edit")
        self.calibration_file_options_layout_3.addWidget(self.save_matrices_file_edit)
        self.calculate_matrices_opt_layout.addLayout(self.calibration_file_options_layout_3)
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 480, 461, 51))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayoutWidget = QtGui.QWidget(self.groupBox_3)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 411, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.calibration_file_options_layout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.calibration_file_options_layout.setContentsMargins(0, 0, 0, 0)
        self.calibration_file_options_layout.setObjectName("calibration_file_options_layout")
        self.select_calibration_file_button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.select_calibration_file_button.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_calibration_file_button.sizePolicy().hasHeightForWidth())
        self.select_calibration_file_button.setSizePolicy(sizePolicy)
        self.select_calibration_file_button.setObjectName("select_calibration_file_button")
        self.calibration_file_options_layout.addWidget(self.select_calibration_file_button)
        self.select_matrices_file_edit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.select_matrices_file_edit.setEnabled(True)
        self.select_matrices_file_edit.setReadOnly(True)
        self.select_matrices_file_edit.setObjectName("select_matrices_file_edit")
        self.calibration_file_options_layout.addWidget(self.select_matrices_file_edit)
        self.formLayoutWidget = QtGui.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 580, 421, 31))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout_3 = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.matching_file_button = QtGui.QPushButton(self.formLayoutWidget)
        self.matching_file_button.setEnabled(False)
        self.matching_file_button.setObjectName("matching_file_button")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.matching_file_button)
        self.matching_file_edit = QtGui.QLineEdit(self.formLayoutWidget)
        self.matching_file_edit.setEnabled(False)
        self.matching_file_edit.setReadOnly(True)
        self.matching_file_edit.setObjectName("matching_file_edit")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.matching_file_edit)
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(40, 530, 331, 41))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.match_by_location_radio = QtGui.QRadioButton(self.groupBox_4)
        self.match_by_location_radio.setGeometry(QtCore.QRect(0, 0, 191, 22))
        self.match_by_location_radio.setChecked(True)
        self.match_by_location_radio.setObjectName("match_by_location_radio")
        self.match_by_file_radio = QtGui.QRadioButton(self.groupBox_4)
        self.match_by_file_radio.setGeometry(QtCore.QRect(0, 20, 181, 22))
        self.match_by_file_radio.setObjectName("match_by_file_radio")
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.ok_button, QtCore.SIGNAL("clicked()"), Dialog.ok_pressed)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL("clicked()"), Dialog.close)
        QtCore.QObject.connect(self.select_calibration_file_button, QtCore.SIGNAL("clicked()"), Dialog.use_matrices_from_file_clicked)
        QtCore.QObject.connect(self.radio_calculate_matrices, QtCore.SIGNAL("clicked()"), Dialog.calculate_matrices_radio_clicked)
        QtCore.QObject.connect(self.radio_use_file_matrices, QtCore.SIGNAL("clicked()"), Dialog.select_matrices_radio_clicked)
        QtCore.QObject.connect(self.tv_calibration_files_button, QtCore.SIGNAL("clicked()"), Dialog.select_tv_calib_files_clicked)
        QtCore.QObject.connect(self.matrices_save_button, QtCore.SIGNAL("clicked()"), Dialog.save_matrices_to_file_clicked)
        QtCore.QObject.connect(self.rgb_calibration_files_button, QtCore.SIGNAL("clicked()"), Dialog.select_rgb_calib_files_clicked)
        QtCore.QObject.connect(self.match_by_file_radio, QtCore.SIGNAL("clicked()"), Dialog.match_photos_by_file_radio_clicked)
        QtCore.QObject.connect(self.match_by_location_radio, QtCore.SIGNAL("clicked()"), Dialog.match_photos_by_location_radio_clicked)
        QtCore.QObject.connect(self.matching_file_button, QtCore.SIGNAL("clicked()"), Dialog.on_select_matching_file_button_clicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Relative Photo Alignment", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_button.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_calculate_matrices.setText(QtGui.QApplication.translate("Dialog", "Calculate matrices", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_use_file_matrices.setText(QtGui.QApplication.translate("Dialog", "Use calibration matrices from file", None, QtGui.QApplication.UnicodeUTF8))
        self.rgb_calibration_files_button.setText(QtGui.QApplication.translate("Dialog", "Select camera-1 chessboard photos", None, QtGui.QApplication.UnicodeUTF8))
        self.tv_calibration_files_button.setText(QtGui.QApplication.translate("Dialog", "Select camera-2 chessboard photos", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Chessboard cell size (meters)", None, QtGui.QApplication.UnicodeUTF8))
        self.cell_size_edit.setText(QtGui.QApplication.translate("Dialog", "0.1", None, QtGui.QApplication.UnicodeUTF8))
        self.rgb_tv_table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Dialog", "Camera-1 photo", None, QtGui.QApplication.UnicodeUTF8))
        self.rgb_tv_table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "Camera-2 photo", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Corresponding chessboard photos:", None, QtGui.QApplication.UnicodeUTF8))
        self.matrices_save_button.setText(QtGui.QApplication.translate("Dialog", "Save calibration to file...", None, QtGui.QApplication.UnicodeUTF8))
        self.select_calibration_file_button.setText(QtGui.QApplication.translate("Dialog", "Select calibration file", None, QtGui.QApplication.UnicodeUTF8))
        self.matching_file_button.setText(QtGui.QApplication.translate("Dialog", "Select file containing matching", None, QtGui.QApplication.UnicodeUTF8))
        self.match_by_location_radio.setText(QtGui.QApplication.translate("Dialog", "Match photos by location", None, QtGui.QApplication.UnicodeUTF8))
        self.match_by_file_radio.setText(QtGui.QApplication.translate("Dialog", "Match photos using file", None, QtGui.QApplication.UnicodeUTF8))


import PhotoScan as ps
import sys
from PySide.QtCore import *
from PySide.QtGui import *

doc = ps.app.document
qtapp = QApplication.instance()
label = QLabel("Hello World")

class Form(QDialog):
    def __init__ (self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.button = QPushButton("Apply")
        # Create layout and add widgets
        self.layout = QGridLayout()

        # Set dialog layout
        self.setLayout(self.layout)

        self.button.clicked.connect(self.apply)

        self.groupBox = QGroupBox("Select thermal and rgb photos matching")

        self.radio1 = QRadioButton("&Match by name")
        self.radio2 = QRadioButton("M&atch by photos coordinates")

        self.radio1.clicked.connect(self.by_names_clicked)
        self.radio2.clicked.connect(self.by_distance_clicked)

        self.radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)
        vbox.addStretch(1)
        self.groupBox.setLayout(vbox)

        '''self.label = QLabel("Insert here rgb photo name prefix and corresponding thermal photo name prefix.")
        self.label.setWordWrap(True);
        self.label.setMaximumWidth(300);'''

        hor_layout1 = QHBoxLayout()
        self.label_rgb_1 = QLabel("RGB prefix:")
        self.label_rgb_2 = QLabel("RGB index:")
        self.edit_rgb_prefix = QLineEdit("")
        self.edit_rgb_index = QLineEdit("")
        self.edit_rgb_index.setValidator(QIntValidator(0, 1000000000, self))
        hor_layout1.addWidget(self.label_rgb_1)
        hor_layout1.addWidget(self.edit_rgb_prefix)
        hor_layout1.addWidget(self.label_rgb_2)
        hor_layout1.addWidget(self.edit_rgb_index)

        hor_layout2 = QHBoxLayout()
        self.label_tv_1 = QLabel("TV prefix:")
        self.label_tv_2 = QLabel("TV index:")
        self.edit_tv_prefix = QLineEdit("")
        self.edit_tv_index = QLineEdit("")
        self.edit_tv_index.setValidator(QIntValidator(0, 1000000000, self))
        hor_layout2.addWidget(self.label_tv_1)
        hor_layout2.addWidget(self.edit_tv_prefix)
        hor_layout2.addWidget(self.label_tv_2)
        hor_layout2.addWidget(self.edit_tv_index)

        self.opt_layout = QVBoxLayout()
        self.opt_layout.addLayout(hor_layout1)
        self.opt_layout.addLayout(hor_layout2)

        self.layout.addWidget(self.groupBox)
        self.layout.addLayout(self.opt_layout, 1, 0)
        self.layout.addWidget(self.button)

        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.optional_widgets = [self.label_rgb_1, self.label_tv_1, self.label_rgb_2, self.label_tv_2, self.edit_rgb_prefix, self.edit_rgb_index, self.edit_tv_prefix, self.edit_tv_index]

    def apply(self):
        if self.radio1.isChecked():
            rgb_prefix = self.edit_rgb_prefix.text()
            tv_prefix = self.edit_tv_prefix.text()
            try:
                rgb_index = int(self.edit_rgb_index.text())
                tv_index = int(self.edit_tv_index.text())
            except:
                ps.app.messageBox("Index fields can't be blank!")
                return
            print(lines_tv)
        else:
            print('by distance')
        self.hide()

    def by_names_clicked(self):
        for w in self.optional_widgets:
            w.show()

    def by_distance_clicked(self):
        for w in self.optional_widgets:
            w.hide()
 
def f():
    form.show()

ps.app.addMenuItem("Workflow/Build Thermal Texture...", f)
form = Form()

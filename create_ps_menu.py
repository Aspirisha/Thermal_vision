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

        self.label = QLabel("Insert here rgb photo name and corresponding thermal photo name. Photo name prefix, index, and suffix should be delimetered with space.")
        self.label.setWordWrap(True);
        self.label.setMaximumWidth(300);
        self.edit_rgb_name = QLineEdit("")
        self.edit_tv_name = QLineEdit("")

        hor_layout1 = QHBoxLayout()
        self.label1 = QLabel("Rgb name:")
        self.label2 = QLabel("Rgb name:")
        hor_layout1.addWidget(self.label1)
        hor_layout1.addWidget(self.edit_rgb_name)
        hor_layout2 = QHBoxLayout()
        hor_layout2.addWidget(self.label2)
        hor_layout2.addWidget(self.edit_tv_name)

        self.opt_layout = QVBoxLayout()
        self.opt_layout.addWidget(self.label)
        self.opt_layout.addLayout(hor_layout1)
        self.opt_layout.addLayout(hor_layout2)

        self.layout.addWidget(self.groupBox)
        self.layout.addLayout(self.opt_layout, 1, 0)
        self.layout.addWidget(self.button)

        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.optional_widgets = [self.label, self.label1, self.label2, self.edit_rgb_name, self.edit_tv_name]

    def apply(self):
        if self.radio1.isChecked():
            rgb_name = self.edit_rgb_name.text()
            tv_name = self.edit_rgb_name.text()
            print(rgb_name)
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

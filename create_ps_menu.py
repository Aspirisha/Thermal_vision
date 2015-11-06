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

        self.edit_rgb_name = QLineEdit("rgb photo name")
        self.edit_tv_name = QLineEdit("corresponding thermal photo name")

        self.layout.addWidget(self.groupBox)
        self.layout.addWidget(self.edit_rgb_name)
        self.layout.addWidget(self.edit_tv_name)
        self.layout.addWidget(self.button)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
    # Greets the user
    def apply(self):
        pass

    def by_names_clicked(self):
        self.edit_rgb_name.show()
        self.edit_tv_name.show()
    def by_distance_clicked(self):
        self.edit_rgb_name.hide()
        self.edit_tv_name.hide()
 
def f():
    form.show()

ps.app.addMenuItem("Workflow/Build Thermal Texture...", f)
form = Form()

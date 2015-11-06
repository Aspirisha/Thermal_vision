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
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)
 
    # Greets the user
    def greetings(self):
        print ("Hello s" + self.edit.text())
 
def f():
    global label
    # Create the Qt Application
    # Create and show the form
    #form = Form()
    #form.show()
    label.show()
    print('here')
    # Run the main Qt loop

if __name__ == '__main__': sys.modules['create_ps_menu'] = sys.modules['__main__']

ps.app.addMenuItem("Workflow/Build Thermal Texture...", f)

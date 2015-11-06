import sys
from PySide.QtCore import *
from PySide.QtGui import *
 
# Create a Qt application
app = QApplication.instance()
# Create a Label and show it
label = QLabel("Hello World")
label.show()
# Enter Qt application main loop
#sys.exit(app.exec_())
#sys.exit()
if __name__ == '__main__': sys.modules['asgard'] = sys.modules['__main__']
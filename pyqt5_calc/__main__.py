"""PyQt5 Calculator"""
from .calc import *

if __name__ == "__main__":
    app = QApplication([])

    window = PyQt5Calculator()
    window.show()

    app.exec()
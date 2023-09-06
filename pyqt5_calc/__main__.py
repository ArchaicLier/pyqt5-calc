"""PyQt5 Calculator"""
from PyQt5.QtWidgets import QApplication

from calc import PyQt5Calculator

if __name__ == "__main__":
    app = QApplication([])

    window = PyQt5Calculator()
    window.show()

    app.exec()

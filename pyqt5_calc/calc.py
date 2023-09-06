"""PyQt5 Calculator"""
from functools import partial

from ast import literal_eval

from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLineEdit,\
    QPushButton, QWidget

from PyQt5.QtCore import Qt

class PyQt5Calculator(QMainWindow):
    """MainWindow Class that contains all methods and params for calculator"""

    def __init__(self, parent = None) -> None:
        super().__init__(parent = parent)

        button_size = 30

        #Buttons layout
        self.buttons_layout = {} # type: dict[str,QPushButton]
        buttons_layout = [
            ['7','8','9','/','C'],
            ['4','5','6','*','('],
            ['1','2','3','-',')'],
            ['0','00','.','+','=']
        ]

        self.setMaximumSize(0,0)
        self.setWindowTitle('Какулятор')

        # Central Widget
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit,0,0,1,len(buttons_layout[0]))

        for row, keys in enumerate(buttons_layout):
            for col, key in enumerate(keys):
                self.buttons_layout[key] = QPushButton(key)
                self.buttons_layout[key].setFixedSize(button_size,button_size)
                layout.addWidget(self.buttons_layout[key],row+1,col)

        self._bind_key()

        self.setCentralWidget(widget)

    def _bind_key(self):
        for key,button in self.buttons_layout.items():
            if key not in ('C','='):
                button.clicked.connect(partial(self._add_text,key))
        self.buttons_layout['C'].clicked.connect(self._clear_line)

        self.buttons_layout['='].clicked.connect(self._eval_line)
        self.line_edit.returnPressed.connect(self._eval_line)

    def _eval_line(self):
        line_text = self.line_edit.text()
        try:
            line_text = literal_eval(line_text)
            self.line_edit.setText(str(line_text))
        except ValueError:
            self.line_edit.setText('ERROR')

    def _clear_line(self):
        self.line_edit.setText('')

    def _add_text(self,text:str) -> None:
        line_text = self.line_edit.text() + text
        self.line_edit.setText(line_text)

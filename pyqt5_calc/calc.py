"""PyQt5 Calculator"""
from functools import partial
from math import pi,sqrt

import subprocess

from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLineEdit,\
    QPushButton, QWidget

from PyQt5.QtCore import Qt

from . import plugins_manager

class PyQt5Calculator(QMainWindow):
    """MainWindow Class that contains all methods and params for calculator"""

    def __init__(self, parent = None) -> None:
        super().__init__(parent = parent)

        self.plugins_manager = plugins_manager.PluginsManager(self)

        button_size = 30

        #Buttons layout
        self.buttons_layout = {} # type: dict[str,QPushButton]
        buttons_layout = [
            ['7','8','9','/','C','pi'],
            ['4','5','6','*','(','sqrt'],
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

    def _show_plugins(self):
        return self.plugins_manager.available_plugins.keys()
    
    def _load_plugin(self,plugin_name):
        return self.plugins_manager.load_plugin(plugin_name)

    def _bind_key(self):
        for key,button in self.buttons_layout.items():
            if key not in ('C','=','sqrt'):
                button.clicked.connect(partial(self._add_text,key))

        self.buttons_layout['sqrt'].clicked.connect(partial(self._add_text,'sqrt('))

        self.buttons_layout['C'].clicked.connect(self._clear_line)

        self.buttons_layout['='].clicked.connect(self._eval_line)
        self.line_edit.returnPressed.connect(self._eval_line)

    def _eval_line(self):
        
        line_text = self.line_edit.text()
        if line_text[0] == '/':
            try:
                exec(line_text[1:])
                self.line_edit.setText('Executed')
            except:
                self.line_edit.setText('ERROR')
        elif line_text[0] == '!':
            with subprocess.Popen(line_text[1:].split(' '), stdout=subprocess.PIPE) as proc:
                for line in proc.stdout.readlines():
                    print(line.decode())
                    self.line_edit.setText(line.decode())
        else:
            try:
                line_text = eval(line_text)
                self.line_edit.setText(str(line_text))
            except:
                self.line_edit.setText('ERROR')

    def _clear_line(self):
        self.line_edit.setText('')

    def _add_text(self,text:str) -> None:
        line_text = self.line_edit.text() + text
        self.line_edit.setText(line_text)

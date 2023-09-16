from abc import ABC, abstractmethod
import importlib
import pkgutil
from re import I
import typing

import pyqt5_calc.plugins

from .calc import PyQt5Calculator

from PyQt5.QtWidgets import QAction, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QWidget, QVBoxLayout

class AbstractPlugin(ABC):
    """Plugin abstract class"""

    @property
    @abstractmethod
    def _version(self) -> str:
        """Plugin version"""
        ...

    @property
    @abstractmethod
    def _about(self) -> str:
        """Plugins about"""
        ...

    @property
    @abstractmethod
    def _authors(self) -> str:
        """Plugin author"""
        ...

    @abstractmethod
    def load_plugin(self, window:PyQt5Calculator) -> None:
        """Method loads plugin

        Args:
            window (PyQt5Calculator): window
        """
        ...

class PluginsManagerWindow(QMainWindow):
    def __init__(self, manager, parent=None) -> None:
        super().__init__(parent)

        widget = QWidget()
        layout = QVBoxLayout(widget)

        qlist_plguins = QListWidget()
        layout.addWidget(qlist_plguins)

        item_test = QListWidgetItem('Test')

        qlist_plguins.addItem(item_test)
        qlist_plguins.itemClicked.connect(self._item_clicked)

        self.setCentralWidget(widget)

    def _item_clicked(self,item:QListWidgetItem):
        print(item.text())


class PluginsManager():
    """Plugins manager window"""

    def __init__(self, window:PyQt5Calculator) -> None:

        self.window = window

        self.loaded_plugins = {}

        self.available_plugins = {
            name: importlib.import_module(pyqt5_calc.plugins.__name__+'.'+name)
            for finder, name, ispkg
            in pkgutil.iter_modules(pyqt5_calc.plugins.__path__)
        }

        self.window_plugins = PluginsManagerWindow(self)
        self.window_plugins.show()

    def load_plugin(self, plugin_name) -> str:
        if plugin_name in self.loaded_plugins:
            return 'Plugin already loaded'
        if plugin_name in self.available_plugins:
            plugin = self.available_plugins[plugin_name].Plugin()# type: AbstractPlugin

            plugin.load_plugin(self.window)

            self.loaded_plugins[plugin_name] = plugin
            
            return 'Plugin loaded'

        return 'No named plugin'



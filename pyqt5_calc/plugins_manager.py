from abc import ABC, abstractmethod
import importlib
import pkgutil
import typing
import inspect

import pyqt5_calc.plugins

from .calc import PyQt5Calculator

from PyQt5.QtWidgets import QAction, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QWidget, QVBoxLayout

class AbstractPlugin(ABC):
    """Plugin abstract class"""

    @classmethod
    @abstractmethod
    def _name(cls)->str:
        """Plugin name"""

    @classmethod
    @abstractmethod
    def _version(cls) -> str:
        """Plugin version"""

    @classmethod
    @abstractmethod
    def _about(cls) -> str:
        """Plugins about"""

    @classmethod
    @abstractmethod
    def _authors(cls) -> str:
        """Plugin author"""

    @abstractmethod
    def load_plugin(self, window:PyQt5Calculator) -> None:
        """Method loads plugin

        Args:
            window (PyQt5Calculator): window
        """

class PluginItem(QListWidgetItem):

    def __init__(self, plugin:typing.Type[AbstractPlugin], parent:typing.Optional[QWidget]=None) -> None:
        super().__init__(parent=parent)

        self.setText(plugin._name())

        self.plugin = plugin


class PluginsManager():
    """Plugins manager window"""

    def __init__(self, window:PyQt5Calculator) -> None:

        self.window = window

        self.loaded_plugins = {}

        self.available_modules = {
            name: importlib.import_module(pyqt5_calc.plugins.__name__+'.'+name)
            for finder, name, ispkg
            in pkgutil.iter_modules(pyqt5_calc.plugins.__path__)
        }

        self.available_plugins = {} # type: typing.Dict[str, PluginItem]

        for module_name,module in self.available_modules.items():
            for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(class_obj,AbstractPlugin) and class_obj != AbstractPlugin:
                    self.available_plugins['{}.{}'.format(module_name,class_name)] = PluginItem(class_obj)

        self.window_plugins = PluginsManagerWindow(self)
        self.window_plugins.show()

    def load_plugin(self, plugin: typing.Type[AbstractPlugin]) -> int:
        if plugin in self.loaded_plugins:
            return 0
        else:
            loaded_plugin = plugin()
            loaded_plugin.load_plugin(self.window)
            self.loaded_plugins[plugin] = loaded_plugin
            return 1


class PluginsManagerWindow(QMainWindow):
    def __init__(self, manager: PluginsManager, parent=None) -> None:
        super().__init__(parent)

        self.manager = manager

        widget = QWidget()
        layout = QVBoxLayout(widget)

        qlist_plguins = QListWidget()
        layout.addWidget(qlist_plguins)
        qlist_plguins.itemClicked.connect(self._item_clicked)


        for name,plugin in manager.available_plugins.items():
            qlist_plguins.addItem(plugin)

        self.setCentralWidget(widget)

    def _item_clicked(self,item:PluginItem):
        if (self.manager.load_plugin(item.plugin)):
            item.setText(item.text()+'(loaded)')

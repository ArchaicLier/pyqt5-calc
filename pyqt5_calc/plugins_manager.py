from abc import ABC, abstractmethod
import importlib
import pkgutil
import typing

import pyqt5_calc.plugins

from .calc import PyQt5Calculator

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

    def load_plugin(self, plugin_name) -> str:
        if plugin_name in self.loaded_plugins:
            return 'Plugin already loaded'
        if plugin_name in self.available_plugins:
            plugin = self.available_plugins[plugin_name].Plugin()# type: AbstractPlugin

            plugin.load_plugin(self.window)

            self.loaded_plugins[plugin_name] = plugin
            
            return 'Plugin loaded'

        return 'No named plugin'



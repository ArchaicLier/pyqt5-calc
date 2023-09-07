from pyqt5_calc.plugins_manager import AbstractPlugin
import pyqt5_calc.calc
import typing

class Plugin(AbstractPlugin):

    @property
    def _version(self) -> str:
        return '1.0.0'
    
    @property
    def _authors(self) -> str:
        return 'Archaic Lier'

    @property
    def _about(self) -> str:
        return """Example plugin:
        Resize buttons
        """

    def load_plugin(self, window:pyqt5_calc.calc.PyQt5Calculator) -> None:
        """Change buttons size"""
        for key,button in window.buttons_layout.items():
            button.setFixedSize(50,50)


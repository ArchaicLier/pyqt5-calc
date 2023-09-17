from pyqt5_calc.plugins_manager import AbstractPlugin
import pyqt5_calc.calc

class Plugin(AbstractPlugin):

    @staticmethod
    def _name() -> str:
        return 'Resize Buttons'

    @staticmethod
    def _version() -> str:
        return '1.0.0'
    
    @staticmethod
    def _authors() -> str:
        return 'Archaic Lier'

    @staticmethod
    def _about() -> str:
        return """Example plugin: Resize buttons"""

    def load_plugin(self, window:pyqt5_calc.calc.PyQt5Calculator) -> None:
        """Change buttons size"""
        for key,button in window.buttons_layout.items():
            button.setFixedSize(50,50)

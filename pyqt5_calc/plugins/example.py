from pyqt5_calc.plugins_manager import AbstractPlugin
import pyqt5_calc.calc

class ResizeButtonPlugin(AbstractPlugin):

    @classmethod
    def _name(cls) -> str:
        return 'Resize Buttons'

    @classmethod
    def _version(cls) -> str:
        return '1.0.0'
    
    @classmethod
    def _authors(cls) -> str:
        return 'Archaic Lier'

    @classmethod
    def _about(cls) -> str:
        return """Example plugin: Resize buttons"""

    def load_plugin(self, window:pyqt5_calc.calc.PyQt5Calculator) -> None:
        """Change buttons size"""
        for key,button in window.buttons_layout.items():
            button.setFixedSize(50,50)

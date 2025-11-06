"""
Widget gerenciador de Kexts
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class KextManagerWidget(QWidget):
    """Widget para gerenciamento de kexts"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        
        title = QLabel("Gerenciador de Kexts")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        desc = QLabel("Gerenciador de kexts será implementado aqui.")
        layout.addWidget(desc)
        
        layout.addStretch()


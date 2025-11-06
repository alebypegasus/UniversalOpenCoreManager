"""
Classe principal da aplicação com configurações de estilo
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor


class UOCMApplication:
    """Classe para configuração da aplicação"""
    
    @staticmethod
    def setup_styles(app: QApplication) -> None:
        """Configura o estilo Liquid Glass da aplicação"""
        app.setStyle("Fusion")
        
        # Configurar paleta de cores Liquid Glass
        palette = QPalette()
        
        # Cores base (macOS Tahoe style)
        bg_color = QColor(30, 30, 30, 230)  # Fundo translúcido escuro
        fg_color = QColor(255, 255, 255, 255)  # Texto branco
        accent_color = QColor(0, 122, 255, 255)  # Azul sistema macOS
        secondary_color = QColor(100, 100, 100, 200)
        
        # Window
        palette.setColor(QPalette.ColorRole.Window, bg_color)
        palette.setColor(QPalette.ColorRole.WindowText, fg_color)
        
        # Base
        palette.setColor(QPalette.ColorRole.Base, QColor(40, 40, 40, 240))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50, 240))
        
        # Text
        palette.setColor(QPalette.ColorRole.Text, fg_color)
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        
        # Button
        palette.setColor(QPalette.ColorRole.Button, secondary_color)
        palette.setColor(QPalette.ColorRole.ButtonText, fg_color)
        
        # Highlight
        palette.setColor(QPalette.ColorRole.Highlight, accent_color)
        palette.setColor(QPalette.ColorRole.HighlightedText, fg_color)
        
        # Link
        palette.setColor(QPalette.ColorRole.Link, accent_color)
        palette.setColor(QPalette.ColorRole.LinkVisited, QColor(175, 82, 222, 255))
        
        app.setPalette(palette)
        
        # Configurar fonte
        font = QFont("SF Pro Display", 13)
        font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
        app.setFont(font)
        
        # Estilo CSS adicional para efeitos glass
        app.setStyleSheet("""
            QMainWindow {
                background-color: rgba(30, 30, 30, 230);
                border-radius: 12px;
            }
            
            QWidget {
                background-color: transparent;
                color: white;
            }
            
            QPushButton {
                background-color: rgba(100, 100, 100, 200);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: rgba(120, 120, 120, 220);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            QPushButton:pressed {
                background-color: rgba(80, 80, 80, 240);
            }
            
            QPushButton:disabled {
                background-color: rgba(60, 60, 60, 150);
                color: rgba(150, 150, 150, 255);
            }
            
            QLineEdit, QTextEdit, QPlainTextEdit {
                background-color: rgba(40, 40, 40, 240);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                padding: 6px;
            }
            
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border: 1px solid rgba(0, 122, 255, 0.5);
            }
            
            QTreeView, QListView, QTableView {
                background-color: rgba(40, 40, 40, 200);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                selection-background-color: rgba(0, 122, 255, 0.3);
            }
            
            QScrollBar:vertical {
                background: rgba(40, 40, 40, 200);
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: rgba(100, 100, 100, 200);
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: rgba(120, 120, 120, 240);
            }
            
            QToolTip {
                background-color: rgba(50, 50, 50, 240);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                padding: 4px 8px;
            }
        """)


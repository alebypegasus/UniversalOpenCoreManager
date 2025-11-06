"""
Main entry point for UOCM application
Ponto de entrada principal da aplicação UOCM
"""

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from uocm.core.app import UOCMApplication
from uocm.core.config import Config
from uocm.core.i18n import tr
from uocm.ui.main_window import MainWindow
from uocm.db.init_data import init_database


def main() -> int:
    """
    Main entry function for the application
    Função principal de entrada da aplicação
    """
    # Configure resource paths
    # Configurar caminhos de recursos
    app_path = Path(__file__).parent.parent
    Config.set_app_path(app_path)
    
    # Initialize database with initial data
    # Inicializar banco de dados com dados iniciais
    try:
        init_database()
    except Exception as e:
        print(f"Warning: Error initializing database: {e}")
        print(f"Aviso: Erro ao inicializar banco de dados: {e}")
    
    # Create Qt application
    # Criar aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName("UOCM")
    app.setOrganizationName(tr("app.organization"))
    app.setApplicationVersion(tr("app.version"))
    
    # Configure theme and style
    # Configurar tema e estilo
    UOCMApplication.setup_styles(app)
    
    # Create main window
    # Criar janela principal
    window = MainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

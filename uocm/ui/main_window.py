"""
Janela principal da aplicação
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QTreeView,
    QMenuBar,
    QStatusBar,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon

from uocm.ui.detector_widget import DetectorWidget
from uocm.ui.generator_widget import GeneratorWidget
from uocm.ui.editor_widget import EditorWidget
from uocm.ui.kext_manager_widget import KextManagerWidget
from uocm.core.i18n import tr


class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("app.title"))
        self.setMinimumSize(1200, 800)
        
        self._setup_ui()
        self._setup_menu()
        self._setup_statusbar()
    
    def _setup_ui(self) -> None:
        """Configura interface principal"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked widget para diferentes views
        self.stacked = QStackedWidget()
        layout.addWidget(self.stacked)
        
        # Adicionar widgets
        self.detector_widget = DetectorWidget()
        self.generator_widget = GeneratorWidget()
        self.editor_widget = EditorWidget()
        self.kext_widget = KextManagerWidget()
        
        # Conectar detector ao gerador
        self.detector_widget.hardware_detected.connect(
            self.generator_widget.set_hardware_info
        )
        
        self.stacked.addWidget(self.detector_widget)
        self.stacked.addWidget(self.generator_widget)
        self.stacked.addWidget(self.editor_widget)
        self.stacked.addWidget(self.kext_widget)
        
        # Barra lateral de navegação
        self._setup_sidebar()
        
        # Mostrar detector por padrão
        self.stacked.setCurrentWidget(self.detector_widget)
    
    def _setup_sidebar(self) -> None:
        """Configura barra lateral"""
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: rgba(40, 40, 40, 240);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Botões de navegação
        nav_buttons = [
            (tr("ui.detector.title"), self.detector_widget),
            (tr("ui.generator.title"), self.generator_widget),
            (tr("ui.editor.title"), self.editor_widget),
            (tr("ui.kext_manager.title"), self.kext_widget),
        ]
        
        for text, widget in nav_buttons:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, w=widget: self._navigate_to(w))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Adicionar sidebar ao layout principal
        main_layout = self.centralWidget().layout()
        sidebar_layout = QHBoxLayout()
        sidebar_layout.addWidget(sidebar)
        sidebar_layout.addWidget(self.stacked)
        main_layout.addLayout(sidebar_layout)
    
    def _navigate_to(self, widget: QWidget) -> None:
        """Navega para um widget"""
        self.stacked.setCurrentWidget(widget)
    
    def _setup_menu(self) -> None:
        """Configura menu"""
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu(tr("menu.file"))
        
        new_action = QAction(tr("menu.new_efi"), self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_efi)
        file_menu.addAction(new_action)
        
        open_action = QAction(tr("menu.open_efi"), self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_efi)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(tr("menu.exit"), self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Ajuda
        help_menu = menubar.addMenu(tr("menu.help"))
        
        about_action = QAction(tr("menu.about"), self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_statusbar(self) -> None:
        """Configura barra de status"""
        self.statusBar().showMessage(tr("ui.editor.ready"))
    
    def _new_efi(self) -> None:
        """Cria novo EFI"""
        self.stacked.setCurrentWidget(self.generator_widget)
    
    def _open_efi(self) -> None:
        """Abre EFI existente"""
        from PyQt6.QtWidgets import QFileDialog
        path = QFileDialog.getExistingDirectory(self, "Selecionar EFI")
        if path:
            self.editor_widget.load_efi(path)
            self.stacked.setCurrentWidget(self.editor_widget)
    
    def _show_about(self) -> None:
        """Mostra diálogo sobre"""
        QMessageBox.about(
            self,
            tr("menu.about"),
            f"{tr('app.title')} {tr('app.version')}\n\n"
            "Gerador e gerenciador avançado de EFI para Hackintosh\n\n"
            f"Desenvolvido por {tr('app.organization')}"
        )


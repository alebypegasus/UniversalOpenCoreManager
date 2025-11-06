"""
Widget gerador de EFI
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QTextEdit,
    QProgressBar,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from pathlib import Path

from uocm.engine_generator import EFIGenerator, GenerationMode
from uocm.ui.detector_widget import DetectorWidget


class GenerationThread(QThread):
    """Thread para geração de EFI"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)
    
    def __init__(self, generator, hardware, mode, output_path):
        super().__init__()
        self.generator = generator
        self.hardware = hardware
        self.mode = mode
        self.output_path = output_path
    
    def run(self) -> None:
        try:
            self.progress.emit("Gerando estrutura EFI...")
            efi_path = self.generator.generate_efi(
                self.hardware,
                self.mode,
                self.output_path,
            )
            self.finished.emit(str(efi_path))
        except Exception as e:
            self.error.emit(str(e))


class GeneratorWidget(QWidget):
    """Widget para geração de EFI"""
    
    def __init__(self):
        super().__init__()
        self.hardware_info = None
        self.generator = EFIGenerator()
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel("Gerador Automático de EFI")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel(
            "Gere automaticamente uma estrutura EFI completa baseada no hardware detectado.\n"
            "Selecione o modo de geração e clique em Gerar."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Modo de geração
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Modo:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Conservador", "Padrão", "Agressivo"])
        self.mode_combo.setCurrentIndex(1)  # Padrão
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)
        
        # Botão de geração
        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Gerar EFI")
        self.generate_btn.clicked.connect(self._generate_efi)
        self.generate_btn.setMinimumHeight(40)
        btn_layout.addWidget(self.generate_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Barra de progresso
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Log de geração
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Log de geração aparecerá aqui...")
        layout.addWidget(self.log)
    
    def set_hardware_info(self, hardware):
        """Define hardware detectado"""
        self.hardware_info = hardware
    
    def _generate_efi(self) -> None:
        """Inicia geração de EFI"""
        if not self.hardware_info:
            QMessageBox.warning(
                self,
                "Hardware não detectado",
                "Por favor, detecte o hardware primeiro na aba Detector."
            )
            return
        
        # Determinar modo
        mode_map = {
            0: GenerationMode.CONSERVATIVE,
            1: GenerationMode.STANDARD,
            2: GenerationMode.AGGRESSIVE,
        }
        mode = mode_map[self.mode_combo.currentIndex()]
        
        self.generate_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.log.clear()
        self.log.append("Iniciando geração de EFI...")
        
        self.thread = GenerationThread(
            self.generator,
            self.hardware_info,
            mode,
            None,
        )
        self.thread.finished.connect(self._on_generation_finished)
        self.thread.error.connect(self._on_generation_error)
        self.thread.progress.connect(self._on_generation_progress)
        self.thread.start()
    
    def _on_generation_finished(self, efi_path: str) -> None:
        """Callback quando geração termina"""
        self.generate_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.log.append(f"\nEFI gerado com sucesso em: {efi_path}")
        
        QMessageBox.information(
            self,
            "EFI Gerado",
            f"EFI gerado com sucesso!\n\nLocalização: {efi_path}"
        )
    
    def _on_generation_error(self, error: str) -> None:
        """Callback de erro na geração"""
        self.generate_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.log.append(f"\nErro: {error}")
        
        QMessageBox.critical(
            self,
            "Erro na Geração",
            f"Erro ao gerar EFI:\n{error}"
        )
    
    def _on_generation_progress(self, message: str) -> None:
        """Callback de progresso"""
        self.log.append(message)


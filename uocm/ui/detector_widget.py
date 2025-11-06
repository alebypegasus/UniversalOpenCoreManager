"""
Widget de detecção de hardware
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QProgressBar,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject

from uocm.detector import HardwareDetector


class DetectionThread(QThread):
    """Thread para detecção de hardware"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def run(self) -> None:
        try:
            detector = HardwareDetector()
            hardware = detector.detect_all()
            self.finished.emit(hardware)
        except Exception as e:
            self.error.emit(str(e))


class DetectorWidget(QWidget):
    """Widget para detecção de hardware"""
    
    hardware_detected = pyqtSignal(object)  # Sinal emitido quando hardware é detectado
    
    def __init__(self):
        super().__init__()
        self.hardware_info = None
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel("Detecção de Hardware")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel(
            "Clique no botão abaixo para detectar automaticamente o hardware do sistema.\n"
            "As informações serão usadas para gerar recomendações de EFI."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Botão de detecção
        btn_layout = QHBoxLayout()
        self.detect_btn = QPushButton("Detectar Hardware")
        self.detect_btn.clicked.connect(self._detect_hardware)
        self.detect_btn.setMinimumHeight(40)
        btn_layout.addWidget(self.detect_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Barra de progresso
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Área de resultados
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setPlaceholderText("Resultados da detecção aparecerão aqui...")
        layout.addWidget(self.results)
        
        layout.addStretch()
    
    def _detect_hardware(self) -> None:
        """Inicia detecção de hardware"""
        self.detect_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminado
        self.results.clear()
        
        self.thread = DetectionThread()
        self.thread.finished.connect(self._on_detection_finished)
        self.thread.error.connect(self._on_detection_error)
        self.thread.start()
    
    def _on_detection_finished(self, hardware) -> None:
        """Callback quando detecção termina"""
        self.hardware_info = hardware
        self.detect_btn.setEnabled(True)
        self.progress.setVisible(False)
        
        # Exibir resultados
        result_text = self._format_hardware_info(hardware)
        self.results.setPlainText(result_text)
        
        # Emitir sinal para atualizar outros widgets
        self.hardware_detected.emit(hardware)
    
    def _on_detection_error(self, error: str) -> None:
        """Callback de erro na detecção"""
        self.detect_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.results.setPlainText(f"Erro na detecção: {error}")
    
    def _format_hardware_info(self, hardware) -> str:
        """Formata informações de hardware para exibição"""
        lines = []
        lines.append("=== Informações de Hardware Detectadas ===\n")
        
        lines.append("CPU:")
        lines.append(f"  Modelo: {hardware.cpu.model}")
        lines.append(f"  Fabricante: {hardware.cpu.vendor}")
        if hardware.cpu.cores:
            lines.append(f"  Núcleos: {hardware.cpu.cores}")
        if hardware.cpu.microarchitecture:
            lines.append(f"  Microarquitetura: {hardware.cpu.microarchitecture}")
        lines.append("")
        
        if hardware.gpu:
            lines.append("GPU:")
            lines.append(f"  Modelo: {hardware.gpu.model}")
            lines.append(f"  Fabricante: {hardware.gpu.vendor}")
            if hardware.gpu.vram:
                lines.append(f"  VRAM: {hardware.gpu.vram} MB")
            lines.append("")
        
        if hardware.network:
            lines.append("Rede:")
            if hardware.network.wifi_model:
                lines.append(f"  Wi-Fi: {hardware.network.wifi_model}")
            if hardware.network.bluetooth_model:
                lines.append(f"  Bluetooth: {hardware.network.bluetooth_model}")
            lines.append("")
        
        if hardware.ram_total_gb:
            lines.append(f"RAM Total: {hardware.ram_total_gb} GB")
            lines.append("")
        
        return "\n".join(lines)


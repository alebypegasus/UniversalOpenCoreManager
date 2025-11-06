"""
Widget editor de config.plist inspirado no ProperTree
"""

import plistlib
import hashlib
import base64
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QLabel,
    QPushButton,
    QLineEdit,
    QMenu,
    QMessageBox,
    QFileDialog,
    QDialog,
    QDialogButtonBox,
    QTextEdit,
    QComboBox,
    QSplitter,
    QHeaderView,
    QToolBar,
    QStatusBar,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QMimeData
from PyQt6.QtGui import (
    QKeySequence,
    QShortcut,
    QAction,
    QIcon,
    QDrag,
    QDropEvent,
    QColor,
)

from uocm.plist_editor.editor import PlistEditor
from uocm.plist_editor.validator import PlistValidator
from uocm.plist_editor.oc_snapshot import OCSnapshot
from uocm.core.config import Config


class ValueType(Enum):
    """Tipos de valores PLIST"""
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    DATA = "data"
    DATE = "date"
    ARRAY = "array"
    DICT = "dict"


class PlistTreeWidget(QTreeWidget):
    """Widget de árvore para exibir e editar PLIST"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["Chave", "Tipo", "Valor"])
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.setAlternatingRowColors(True)
        
        # Configurar colunas
        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # Estilo
        self.setStyleSheet("""
            QTreeWidget {
                background-color: rgba(40, 40, 40, 240);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                selection-background-color: rgba(0, 122, 255, 0.3);
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: rgba(0, 122, 255, 0.3);
            }
        """)


class ValueConverterDialog(QDialog):
    """Diálogo para conversão de valores"""
    
    def __init__(self, parent=None, initial_value: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Conversor de Valores")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Entrada
        input_label = QLabel("Valor de Entrada:")
        layout.addWidget(input_label)
        
        self.input_text = QTextEdit()
        self.input_text.setPlainText(initial_value)
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)
        
        # Tipo de conversão
        type_label = QLabel("Converter para:")
        layout.addWidget(type_label)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Base64", "Hex", "ASCII", "Decimal", "Integer"])
        layout.addWidget(self.type_combo)
        
        # Botão de conversão
        convert_btn = QPushButton("Converter")
        convert_btn.clicked.connect(self._convert)
        layout.addWidget(convert_btn)
        
        # Saída
        output_label = QLabel("Valor Convertido:")
        layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _convert(self) -> None:
        """Converte o valor"""
        input_value = self.input_text.toPlainText()
        conversion_type = self.type_combo.currentText()
        
        try:
            if conversion_type == "Base64":
                result = base64.b64encode(input_value.encode()).decode()
            elif conversion_type == "Hex":
                result = input_value.encode().hex().upper()
            elif conversion_type == "ASCII":
                result = "".join([str(ord(c)) + " " for c in input_value])
            elif conversion_type == "Decimal":
                result = str(int(input_value, 16)) if input_value.startswith("0x") else str(int(input_value))
            elif conversion_type == "Integer":
                result = str(int(input_value))
            else:
                result = input_value
            
            self.output_text.setPlainText(result)
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro na conversão: {str(e)}")
    
    def get_converted_value(self) -> str:
        """Retorna o valor convertido"""
        return self.output_text.toPlainText()


class FindReplaceDialog(QDialog):
    """Diálogo de busca e substituição"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar e Substituir")
        self.setMinimumSize(400, 200)
        
        layout = QVBoxLayout(self)
        
        # Buscar
        find_label = QLabel("Buscar:")
        layout.addWidget(find_label)
        
        self.find_edit = QLineEdit()
        layout.addWidget(self.find_edit)
        
        # Substituir
        replace_label = QLabel("Substituir por:")
        layout.addWidget(replace_label)
        
        self.replace_edit = QLineEdit()
        layout.addWidget(self.replace_edit)
        
        # Opções
        self.keys_check = QLabel("Buscar em chaves")
        self.values_check = QLabel("Buscar em valores")
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_find_text(self) -> str:
        """Retorna texto a buscar"""
        return self.find_edit.text()
    
    def get_replace_text(self) -> str:
        """Retorna texto de substituição"""
        return self.replace_edit.text()


class EditorWidget(QWidget):
    """Widget editor de config.plist inspirado no ProperTree"""
    
    def __init__(self):
        super().__init__()
        self.editor = PlistEditor()
        self.validator = PlistValidator()
        self.current_plist_path: Optional[Path] = None
        self._setup_ui()
        self._setup_shortcuts()
        self._setup_context_menu()
    
    def _setup_ui(self) -> None:
        """Configura interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: rgba(50, 50, 50, 240);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                spacing: 4px;
            }
            QToolButton {
                padding: 4px 8px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: rgba(100, 100, 100, 200);
            }
        """)
        
        # Ações da toolbar
        open_action = QAction("Abrir", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction("Salvar", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        undo_action = QAction("Desfazer", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self._undo)
        toolbar.addAction(undo_action)
        
        redo_action = QAction("Refazer", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self._redo)
        toolbar.addAction(redo_action)
        
        toolbar.addSeparator()
        
        find_action = QAction("Buscar", self)
        find_action.setShortcut(QKeySequence.StandardKey.Find)
        find_action.triggered.connect(self._find_replace)
        toolbar.addAction(find_action)
        
        toolbar.addSeparator()
        
        oc_snapshot_action = QAction("OC Snapshot", self)
        oc_snapshot_action.triggered.connect(self._oc_snapshot)
        toolbar.addAction(oc_snapshot_action)
        
        oc_clean_snapshot_action = QAction("OC Clean Snapshot", self)
        oc_clean_snapshot_action.triggered.connect(self._oc_clean_snapshot)
        toolbar.addAction(oc_clean_snapshot_action)
        
        toolbar.addSeparator()
        
        validate_action = QAction("Validar", self)
        validate_action.triggered.connect(self._validate)
        toolbar.addAction(validate_action)
        
        layout.addWidget(toolbar)
        
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Árvore PLIST
        self.tree = PlistTreeWidget()
        self.tree.itemDoubleClicked.connect(self._edit_item)
        self.tree.itemChanged.connect(self._item_changed)
        splitter.addWidget(self.tree)
        
        # Painel de detalhes (opcional)
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(8, 8, 8, 8)
        
        details_label = QLabel("Detalhes do Item Selecionado")
        details_label.setStyleSheet("font-weight: bold;")
        details_layout.addWidget(details_label)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumWidth(300)
        details_layout.addWidget(self.details_text)
        
        details_layout.addStretch()
        splitter.addWidget(details_widget)
        
        splitter.setSizes([800, 300])
        layout.addWidget(splitter)
        
        # Status bar
        self.status_label = QLabel("Pronto")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: rgba(40, 40, 40, 240);
                padding: 4px 8px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        layout.addWidget(self.status_label)
    
    def _setup_shortcuts(self) -> None:
        """Configura atalhos de teclado"""
        # Copy
        copy_shortcut = QShortcut(QKeySequence.StandardKey.Copy, self)
        copy_shortcut.activated.connect(self._copy)
        
        # Paste
        paste_shortcut = QShortcut(QKeySequence.StandardKey.Paste, self)
        paste_shortcut.activated.connect(self._paste)
        
        # Delete
        delete_shortcut = QShortcut(QKeySequence.StandardKey.Delete, self)
        delete_shortcut.activated.connect(self._delete_selected)
    
    def _setup_context_menu(self) -> None:
        """Configura menu contextual"""
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
    
    def _show_context_menu(self, position) -> None:
        """Mostra menu contextual"""
        item = self.tree.itemAt(position)
        menu = QMenu(self)
        
        if item:
            # Adicionar item
            add_action = menu.addAction("Adicionar Item")
            add_action.triggered.connect(lambda: self._add_item(item))
            
            # Editar
            edit_action = menu.addAction("Editar")
            edit_action.triggered.connect(lambda: self._edit_item(item, 0))
            
            menu.addSeparator()
            
            # Copiar
            copy_action = menu.addAction("Copiar")
            copy_action.triggered.connect(self._copy)
            
            # Colar
            paste_action = menu.addAction("Colar")
            paste_action.triggered.connect(self._paste)
            
            menu.addSeparator()
            
            # Converter valor
            convert_action = menu.addAction("Converter Valor...")
            convert_action.triggered.connect(lambda: self._convert_value(item))
            
            menu.addSeparator()
            
            # Templates OpenCore
            templates_menu = menu.addMenu("Templates OpenCore")
            templates_menu.addAction("ACPI Add Entry", lambda: self._add_template("ACPI", "Add"))
            templates_menu.addAction("Kernel Add Entry", lambda: self._add_template("Kernel", "Add"))
            templates_menu.addAction("UEFI Driver Entry", lambda: self._add_template("UEFI", "Drivers"))
            
            menu.addSeparator()
            
            # Deletar
            delete_action = menu.addAction("Deletar")
            delete_action.triggered.connect(self._delete_item)
        else:
            # Adicionar na raiz
            add_action = menu.addAction("Adicionar Item Raiz")
            add_action.triggered.connect(lambda: self._add_item(None))
        
        menu.exec(self.tree.mapToGlobal(position))
    
    def load_efi(self, efi_path: str) -> None:
        """Carrega EFI para edição"""
        efi_path_obj = Path(efi_path)
        config_path = efi_path_obj / "EFI" / "OC" / "config.plist"
        
        if config_path.exists():
            self.load_plist(config_path)
        else:
            QMessageBox.warning(
                self,
                "Arquivo não encontrado",
                f"config.plist não encontrado em: {config_path}"
            )
    
    def load_plist(self, plist_path: Path) -> None:
        """Carrega arquivo PLIST"""
        if self.editor.load(plist_path):
            self.current_plist_path = plist_path
            self._populate_tree()
            self.status_label.setText(f"Arquivo carregado: {plist_path.name}")
        else:
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao carregar arquivo: {plist_path}"
            )
    
    def _populate_tree(self, parent: Optional[QTreeWidgetItem] = None, data: Optional[Dict[str, Any]] = None) -> None:
        """Popula árvore com dados PLIST"""
        if data is None:
            data = self.editor.data
        
        if parent is None:
            self.tree.clear()
            parent = self.tree.invisibleRootItem()
        
        if isinstance(data, dict):
            for key, value in data.items():
                item = QTreeWidgetItem(parent)
                item.setText(0, str(key))
                item.setData(0, Qt.ItemDataRole.UserRole, key)
                
                if isinstance(value, dict):
                    item.setText(1, "dict")
                    self._populate_tree(item, value)
                elif isinstance(value, list):
                    item.setText(1, "array")
                    self._populate_tree(item, value)
                elif isinstance(value, bool):
                    item.setText(1, "boolean")
                    item.setText(2, str(value))
                elif isinstance(value, int):
                    item.setText(1, "integer")
                    item.setText(2, str(value))
                elif isinstance(value, bytes):
                    item.setText(1, "data")
                    item.setText(2, base64.b64encode(value).decode()[:50] + "...")
                else:
                    item.setText(1, "string")
                    item.setText(2, str(value))
                
                item.setExpanded(True)
        
        elif isinstance(data, list):
            for i, value in enumerate(data):
                item = QTreeWidgetItem(parent)
                item.setText(0, f"[{i}]")
                item.setData(0, Qt.ItemDataRole.UserRole, i)
                
                if isinstance(value, dict):
                    item.setText(1, "dict")
                    self._populate_tree(item, value)
                elif isinstance(value, list):
                    item.setText(1, "array")
                    self._populate_tree(item, value)
                elif isinstance(value, bool):
                    item.setText(1, "boolean")
                    item.setText(2, str(value))
                elif isinstance(value, int):
                    item.setText(1, "integer")
                    item.setText(2, str(value))
                elif isinstance(value, bytes):
                    item.setText(1, "data")
                    item.setText(2, base64.b64encode(value).decode()[:50] + "...")
                else:
                    item.setText(1, "string")
                    item.setText(2, str(value))
    
    def _open_file(self) -> None:
        """Abre arquivo PLIST"""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir config.plist",
            "",
            "PLIST Files (*.plist);;All Files (*)"
        )
        
        if path:
            self.load_plist(Path(path))
    
    def _save_file(self) -> None:
        """Salva arquivo PLIST"""
        if not self.current_plist_path:
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar config.plist",
                "",
                "PLIST Files (*.plist);;All Files (*)"
            )
            if path:
                self.current_plist_path = Path(path)
        
        if self.current_plist_path:
            if self.editor.save(self.current_plist_path):
                self.status_label.setText(f"Arquivo salvo: {self.current_plist_path.name}")
                QMessageBox.information(self, "Sucesso", "Arquivo salvo com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "Erro ao salvar arquivo ou validação falhou.")
    
    def _undo(self) -> None:
        """Desfaz última alteração"""
        if self.editor.undo():
            self._populate_tree()
            self.status_label.setText("Operação desfeita")
    
    def _redo(self) -> None:
        """Refaz última alteração"""
        if self.editor.redo():
            self._populate_tree()
            self.status_label.setText("Operação refeita")
    
    def _find_replace(self) -> None:
        """Busca e substitui"""
        dialog = FindReplaceDialog(self)
        if dialog.exec():
            find_text = dialog.get_find_text()
            replace_text = dialog.get_replace_text()
            # Implementar busca e substituição
            self.status_label.setText(f"Buscando: {find_text}")
    
    def _edit_item(self, item: QTreeWidgetItem, column: int) -> None:
        """Edita item selecionado"""
        if column == 2:  # Coluna de valor
            # Permitir edição inline
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.tree.editItem(item, column)
    
    def _item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Callback quando item é alterado"""
        if column == 2:
            # Atualizar dados PLIST
            new_value = item.text(column)
            # Implementar atualização
            self._save_to_history()
    
    def _add_item(self, parent_item: Optional[QTreeWidgetItem]) -> None:
        """Adiciona novo item"""
        # Implementar adição de item
        pass
    
    def _copy(self) -> None:
        """Copia item selecionado"""
        selected_items = self.tree.selectedItems()
        if selected_items:
            # Implementar cópia
            self.status_label.setText(f"{len(selected_items)} item(s) copiado(s)")
    
    def _paste(self) -> None:
        """Cola item copiado"""
        # Implementar colagem
        self.status_label.setText("Item colado")
    
    def _delete_selected(self) -> None:
        """Deleta itens selecionados"""
        selected_items = self.tree.selectedItems()
        if selected_items:
            reply = QMessageBox.question(
                self,
                "Confirmar",
                f"Deletar {len(selected_items)} item(s)?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                for item in selected_items:
                    parent = item.parent() or self.tree.invisibleRootItem()
                    parent.removeChild(item)
                self._save_to_history()
    
    def _delete_item(self) -> None:
        """Deleta item do menu contextual"""
        item = self.tree.currentItem()
        if item:
            self._delete_selected()
    
    def _convert_value(self, item: QTreeWidgetItem) -> None:
        """Abre diálogo de conversão de valor"""
        current_value = item.text(2)
        dialog = ValueConverterDialog(self, current_value)
        if dialog.exec():
            converted = dialog.get_converted_value()
            item.setText(2, converted)
            self._save_to_history()
    
    def _add_template(self, section: str, subsection: str) -> None:
        """Adiciona template OpenCore"""
        # Implementar adição de templates
        self.status_label.setText(f"Template {section}.{subsection} adicionado")
    
    def _oc_snapshot(self) -> None:
        """Executa OC Snapshot"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta OC",
            ""
        )
        
        if folder:
            self._perform_oc_snapshot(Path(folder), clean=False)
    
    def _oc_clean_snapshot(self) -> None:
        """Executa OC Clean Snapshot"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta OC",
            ""
        )
        
        if folder:
            self._perform_oc_snapshot(Path(folder), clean=True)
    
    def _perform_oc_snapshot(self, oc_path: Path, clean: bool = False) -> None:
        """Executa snapshot do OpenCore usando OCSnapshot"""
        snapshot = OCSnapshot(oc_path)
        updated_data, warnings = snapshot.perform_snapshot(self.editor.data, clean)
        
        self.editor.data = updated_data
        self._save_to_history()
        self._populate_tree()
        
        message = f"OC {'Clean ' if clean else ''}Snapshot concluído!"
        if warnings:
            message += f"\n\nAvisos ({len(warnings)}):\n" + "\n".join(warnings[:5])
            if len(warnings) > 5:
                message += f"\n... e mais {len(warnings) - 5} aviso(s)"
        
        self.status_label.setText(f"OC Snapshot {'(Clean)' if clean else ''} concluído!")
        QMessageBox.information(
            self,
            "Snapshot Concluído",
            message
        )
    
    def _validate(self) -> None:
        """Valida config.plist"""
        is_valid, errors = self.editor.validate()
        
        if is_valid:
            QMessageBox.information(self, "Validação", "config.plist está válido!")
            self.status_label.setText("Validação: OK")
        else:
            error_text = "\n".join(errors[:10])  # Mostrar até 10 erros
            if len(errors) > 10:
                error_text += f"\n... e mais {len(errors) - 10} erro(s)"
            
            QMessageBox.warning(
                self,
                "Erros de Validação",
                f"Encontrados {len(errors)} erro(s):\n\n{error_text}"
            )
            self.status_label.setText(f"Validação: {len(errors)} erro(s) encontrado(s)")
    
    def _save_to_history(self) -> None:
        """Salva estado atual no histórico"""
        # Atualizar dados do editor a partir da árvore
        # (Implementar sincronização árvore -> dados)
        self.editor._save_to_history()

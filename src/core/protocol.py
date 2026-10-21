from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QUndoStack

from src.config import DOCUMENT_PATH
from src.core.commands.file_system_commands import CreateItem, RenameItem, RemoveItem
from src.core.file_system.filesystem_manager import FileSystemManager

if TYPE_CHECKING:
    from src.main_app import MainApp


class Protocol(QObject):
    def __init__(self, parent: Optional[MainApp] = None):
        super().__init__(parent=parent)
        self.ui = parent.ui
        self.file_system_manager = FileSystemManager(root=DOCUMENT_PATH, parent=self)
        self.undo_stack = QUndoStack(self, undoLimit=100)
        self.ui.actionUndo.triggered.connect(self.undo_stack.undo)
        self.ui.actionRedo.triggered.connect(self.undo_stack.redo)

        # Keep their enabled state synchronized
        self.undo_stack.canUndoChanged.connect(
            self.ui.actionUndo.setEnabled
        )
        self.undo_stack.canRedoChanged.connect(
            self.ui.actionRedo.setEnabled
        )

        self.ui.actionUndo.setEnabled(self.undo_stack.canUndo())
        self.ui.actionRedo.setEnabled(self.undo_stack.canRedo())

        self._connect_signals()

    def _connect_signals(self):
        self.ui.treeWidget.create_folder.connect(lambda *x: self.undo_stack.push(CreateItem(self.file_system_manager, *x)))
        self.ui.treeWidget.rename_item.connect(lambda *x: self.undo_stack.push(RenameItem(self.file_system_manager, *x)))
        self.ui.treeWidget.delete_item.connect(lambda *x: self.undo_stack.push(RemoveItem(self.file_system_manager, *x)))
        self.file_system_manager.update_tree_ui.connect(self.ui.treeWidget.refresh_tree)
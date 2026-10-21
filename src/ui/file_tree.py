from typing import Optional
from pathlib import Path
from PySide6.QtCore import Qt, QFileInfo, Signal, Slot, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QTreeWidget, QWidget, QTreeWidgetItem, QStyle, QFileIconProvider, QMenu, QInputDialog, \
    QLineEdit, QMessageBox

from src.core.file_system.file_utils import number_of_elements
from src.ui.context_menu import FileTreeContextMenu


class FileTree(QTreeWidget):
    create_folder = Signal(bool, str)
    rename_item = Signal(str, str)
    cut_item = Signal(str)
    delete_item = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.icon_provider = QFileIconProvider()

        # Context menu
        self.context_menu = FileTreeContextMenu(self)
        self.context_menu.create_action.triggered.connect(self.gui_create_folder)
        self.context_menu.rename_action.triggered.connect(self.gui_rename_item)
        self.context_menu.cut_action.triggered.connect(self.gui_cut_item)
        self.context_menu.delete_action.triggered.connect(self.gui_delete_item)


    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        for action in [
            self.context_menu.rename_action,
            self.context_menu.cut_action,
            self.context_menu.delete_action
        ]:
            action.setEnabled(item is not None)
        self.setCurrentItem(item)

        self.context_menu.exec(event.globalPos())


    def populate_file_tree_widget(self, root: str):
        self.clear()
        try:
            for d in sorted(Path(root).resolve().iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                self._populate_recursive(d, None)
        except PermissionError:
            return

    def _populate_recursive(self, candidate: Path, parent: Optional[QTreeWidgetItem] = None):
        icon = self.icon_provider.icon(QFileInfo(candidate.as_posix()))
        item = QTreeWidgetItem([candidate.name])
        item.setData(
            0,
            Qt.ItemDataRole.UserRole,
            candidate.as_posix()
        )
        item.setIcon(0, icon)
        if parent is None:
            self.addTopLevelItem(item)
        else:
            parent.addChild(item)
        if candidate.is_dir():
            try:
                for d in sorted(candidate.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                    self._populate_recursive(d, item)
            except PermissionError:
                return

    def _get_expanded_paths(self):
        """Save the paths of all expanded items"""
        expanded = set()

        for i in range(self.topLevelItemCount()):
            self._walk(self.topLevelItem(i), expanded, False)

        return expanded

    def _walk(self, item, expanded: set, restore: bool):
        path = item.data(0, Qt.ItemDataRole.UserRole)

        if not restore:
            if item.isExpanded() and path:
                expanded.add(path)
        else:
            if path in expanded:
                item.setExpanded(True)

        for i in range(item.childCount()):
            self._walk(item.child(i), expanded, restore)

    def _restore_expanded_paths(self, expanded: set):
        """Restore expanded items using their stored paths."""
        for i in range(self.topLevelItemCount()):
            self._walk(self.topLevelItem(i), expanded, True)

    @Slot(str)
    def refresh_tree(self, root: str):
        expanded = self._get_expanded_paths()
        self.clear()
        self.populate_file_tree_widget(root)  # Rebuild items
        self._restore_expanded_paths(expanded)

    def gui_create_folder(self):
        item = self.currentItem()
        dialog = QInputDialog(self)
        dialog.setWindowTitle(f"Neue {'K' if not item else 'Subk'}ategorie")
        dialog.setLabelText("Bezeichnung:")
        dialog.setTextEchoMode(QLineEdit.EchoMode.Normal)

        # Forbid path separators and Windows-invalid filename characters
        regex = QRegularExpression(r'[^/\\<>:"|?*]+')
        validator = QRegularExpressionValidator(regex, dialog)

        line_edit = dialog.findChild(QLineEdit)
        line_edit.setValidator(validator)

        if dialog.exec() != QInputDialog.DialogCode.Accepted:
            return
        new = dialog.textValue().strip()

        if not new:
            return

        if item:
            new = Path(item.data(0, Qt.ItemDataRole.UserRole)) / new
        else:
            new = Path(new)
        self.create_folder.emit(item is None, new.as_posix())

    def gui_rename_item(self):
        item = self.currentItem()
        if item is None:
            return
        old_path = Path(item.data(0, Qt.ItemDataRole.UserRole))

        while True:
            dialog = QInputDialog(self)
            dialog.setWindowTitle("Umbenennen")
            dialog.setLabelText(f"Alter Name: {old_path.stem}{f'\nDateiformat: {old_path.suffix}' if old_path.is_file() else ''}\nNeuer Name:")
            dialog.setTextEchoMode(QLineEdit.EchoMode.Normal)

            # Forbid path separators and Windows-invalid filename characters
            regex = QRegularExpression(r'[^/\\<>:"|?*]+')
            validator = QRegularExpressionValidator(regex, dialog)

            line_edit = dialog.findChild(QLineEdit)
            line_edit.setValidator(validator)

            if dialog.exec() != QInputDialog.DialogCode.Accepted:
                return
            name = dialog.textValue().strip()
            name = name + old_path.suffix

            if not name:
                QMessageBox.warning(
                    self,
                    "Warnung",
                    f"Name \"{name}\" ungültig.\nBitte einen gültigen Namen eingeben."
                )
                continue

            if old_path.with_name(name).exists():
                QMessageBox.warning(
                    self,
                    "Warnung",
                    f"Name \"{name}\" existiert bereits! Sie müssen kreativer werden :)"
                )
                continue

            break

        new_path = old_path.with_name(name)
        self.rename_item.emit(old_path.as_posix(), new_path.as_posix())

    def gui_cut_item(self):
        item = self.currentItem()
        self.cut_item.emit(item.data(0, Qt.ItemDataRole.UserRole))


    def gui_delete_item(self):
        item = self.currentItem()
        path_to_delete = item.data(0, Qt.ItemDataRole.UserRole)
        elements, folders, files = number_of_elements(Path(path_to_delete))
        if QMessageBox.question(
                self, "Kategorie löschen", f"Element \"{Path(path_to_delete).name}\" wirklich löschen?\n{elements} Element{'' if elements == 1 else 'e'} ({folders} Kategorie{'' if folders == 1 else 'n'}, {files} Dokument{'' if files == 1 else 'e'})"
        ) == QMessageBox.StandardButton.Yes:
            self.delete_item.emit(path_to_delete)

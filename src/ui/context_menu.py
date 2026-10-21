from typing import Optional
from PySide6.QtWidgets import QMenu, QTreeWidget, QStyle


class FileTreeContextMenu(QMenu):
    def __init__(self, parent: Optional[QTreeWidget] = None):
        super().__init__(parent=parent)
        style = self.parent().style()
        self.create_action = self.addAction(style.standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder), "Neue Kategorie")
        self.rename_action = self.addAction(style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView), "Umbenennen")
        self.cut_action = self.addAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogOkButton), "Ausschneiden")
        self.delete_action = self.addAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton), "Löschen")
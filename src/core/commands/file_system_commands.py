from PySide6.QtGui import QUndoCommand

from src.core.file_system.filesystem_manager import FileSystemManager


class CreateItem(QUndoCommand):
    def __init__(self, filesystem_manager: FileSystemManager, root_child: bool, path: str):
        super().__init__("Neue Kategorie")
        self.filesystem_manager = filesystem_manager
        self.root_child = root_child
        self.path = path
        self.cache_location = None

    def redo(self, /):
        if self.path is not None:
            if self.cache_location is None:
                self.path = self.filesystem_manager.create_item(root_child=self.root_child,
                                                    path=self.path)
            else:
                self.filesystem_manager.retrieve_from_cache(cache_location=self.cache_location,
                                                            destination=self.path)

    def undo(self, /):
        if self.path is not None:
            self.cache_location = self.filesystem_manager.move_to_cache(path=self.path)


class RenameItem(QUndoCommand):
    def __init__(self, filesystem_manager: FileSystemManager, old_path: str, new_path: str):
        super().__init__("Umbenennen")
        self.filesystem_manager = filesystem_manager
        self.old_path = old_path
        self.new_path = new_path

    def redo(self, /):
        self.filesystem_manager.rename_item(old_path=self.old_path,
                                            new_path=self.new_path)

    def undo(self, /):
        self.filesystem_manager.rename_item(old_path=self.new_path,
                                            new_path=self.old_path)


class RemoveItem(QUndoCommand):
    def __init__(self, filesystem_manager: FileSystemManager, path: str):
        super().__init__("Löschen")
        self.filesystem_manager = filesystem_manager
        self.path = path
        self.cache_path = None

    def redo(self, /):
        self.cache_path = self.filesystem_manager.move_to_cache(path=self.path)

    def undo(self, /):
        if self.cache_path is not None:
            self.filesystem_manager.retrieve_from_cache(cache_location=self.cache_path,
                                                        destination=self.path)
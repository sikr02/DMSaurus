import shutil
from typing import Optional
from pathlib import Path
import uuid
from PySide6.QtCore import QObject, Signal

from src.config import CACHE_PATH


class FileSystemManager(QObject):
    update_tree_ui = Signal(str)
    def __init__(self, root: Path, parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self.root = root

    def create_item(self, root_child: bool, path: str):
        if root_child:
            path = self.root / path
        else:
            path = Path(path)
            if not path.is_relative_to(self.root):
                return None

        if path.exists():
            return None

        # if path.suffix:
        #     path.parent.mkdir(parents=True, exist_ok=True)
        #     path.touch(exist_ok=True)
        # else:
        path.mkdir(parents=True, exist_ok=True)
        self.update_tree_ui.emit(self.root.as_posix())
        return path

    def rename_item(self, old_path: str, new_path: str):
        old_path = Path(old_path)
        new_path = Path(new_path)
        if old_path.exists() and not new_path.exists():
            old_path.rename(old_path.with_name(new_path.name))
            self.update_tree_ui.emit(self.root.as_posix())

    def move_to_cache(self, path: str):
        path = Path(path)
        # Unique name prevents collisions
        destination = CACHE_PATH / uuid.uuid4().hex

        shutil.move(path.as_posix(), destination.as_posix())
        self.update_tree_ui.emit(self.root.as_posix())
        return destination

    def retrieve_from_cache(self, cache_location: str, destination: str):
        shutil.move(cache_location, destination)
        self.update_tree_ui.emit(self.root.as_posix())

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dms.database.models import Folder
from src.dms.storage.filesystem import FileStorage


class FolderService:
    def __init__(self, session: Session, storage: FileStorage):
        # Link to database
        self.session = session
        self.storage = storage

    def create_folder(self, name: str, parent_id: int | None = None) -> Folder:
        parent = None
        if parent_id is not None:
            parent = self.get_folder(parent_id)
            if parent is None:
                raise ValueError(f"Parent folder not found: {parent_id}")

        folder = Folder(name=name, parent=parent)
        self.session.add(folder)
        self.session.commit()
        self.session.refresh(folder)
        return folder

    def get_folder(self, folder_id: int) -> Folder | None:
        return self.session.get(Folder, folder_id)

    def get_folder_by_name(self, name: str, parent_id: int | None = None) -> Folder | None:
        statement = select(Folder).where(Folder.name == name, Folder.parent_id == parent_id)
        return self.session.scalar(statement)

    def list_children(self, parent_id: int | None = None) -> list[Folder]:
        statement = select(Folder).where(Folder.parent_id == parent_id).order_by(Folder.name)
        return list(self.session.scalars(statement).all())

    def list_folders(self) -> list[Folder]:
        statement = select(Folder)
        return list(self.session.scalars(statement).all())

    def delete_folder(self, folder_id: int) -> bool:
        # Retrieve folder object from database
        folder = self.get_folder(folder_id)
        # If no folder with the ID exists, delete fails
        if folder is None:
            return False
        self._delete_folder_recursive(folder)
        self.session.commit()
        return True

    def _delete_folder_recursive(self, folder: Folder):
        # Delete all children
        for f in list(folder.children):
            self._delete_folder_recursive(f)
        # Delete all documents
        for d in list(folder.documents):
            stored_filename = d.stored_filename
            # Delete database entry
            self.session.delete(d)
            # Delete file from internal file storage
            self.storage.delete(stored_filename)
        # Delete folder database entry
        self.session.delete(folder)

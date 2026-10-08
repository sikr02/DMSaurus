from pathlib import Path
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dms.database.models import Document, Folder
from src.dms.storage.filesystem import FileStorage


class DocumentService:
    def __init__(self, session: Session, storage: FileStorage):
        # Link to database
        self.session = session
        # Storage manager for file storage
        self.storage = storage

    def create_document(self, source: Path, title: str, folder: Folder) -> Document:
        # Check whether file exists
        if not source.exists():
            raise FileNotFoundError(source)
        # Create "unique" new filepath to store the file
        stored_filename = f"{uuid4()}{source.suffix}"
        # Copy the file to the new location
        self.storage.save(source=source, filename=stored_filename)
        # Create database entry
        document = Document(title=title, stored_filename=stored_filename, folder=folder)
        # Add to database, update database and refresh object to return
        self.session.add(document)
        self.session.commit()
        self.session.refresh(document)
        return document

    def delete_document(self, document_id: int) -> bool:
        # Retrieve document object from database
        document = self.get_document(document_id)
        # If no document with the ID exists, delete fails
        if document is None:
            return False
        stored_filename = document.stored_filename
        # Delete database entry
        self.session.delete(document)
        self.session.commit()
        # Delete file from internal file storage
        self.storage.delete(stored_filename)
        return True

    def get_document(self, document_id: int) -> Document | None:
        return self.session.get(Document, document_id)

    def list_documents(self) -> list[Document]:
        statement = select(Document)
        return list(self.session.scalars(statement).all())

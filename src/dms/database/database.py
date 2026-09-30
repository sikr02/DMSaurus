from datetime import datetime
from sqlalchemy import Sequence, create_engine, select
from sqlalchemy.orm import Session

from src.dms.database.models import Document


DATABASE_URL = "sqlite:///data/dmsaurus.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

def get_session():
    return Session(engine)

def add_document(title: str) -> None:
    with Session(engine) as session:
        document = Document(
            title=title,
            original_filename="a",
            file_path="a",
            file_type="pdf",
            file_size="1024",
            created_at=datetime.now(),
            modified_at=datetime.now()
        )
        session.add(document)
        session.commit()

def get_documents() -> Sequence[Document]:
    with Session(engine) as session:
        statement = select(Document)
        documents = session.scalars(statement).all()

        return documents
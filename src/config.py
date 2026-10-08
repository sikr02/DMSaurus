from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

BASE = Path(__file__).resolve().parent.parent
DATA_PATH = BASE / "data"
DOCUMENT_PATH = DATA_PATH / "documents"
DATABASE_PATH = DATA_PATH / "dmsaurus.db"

DATABASE_URL = f"sqlite:///{str(DATABASE_PATH.as_posix())}"

engine = create_engine(
    DATABASE_URL
)

def get_session():
    return Session(engine)

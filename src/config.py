from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CACHE_PATH = BASE / ".cache"
DATA_PATH = BASE / "data"
DOCUMENT_PATH = DATA_PATH / "documents"
DATABASE_PATH = DATA_PATH / "dmsaurus.db"

DATABASE_URL = f"sqlite:///{str(DATABASE_PATH.as_posix())}"

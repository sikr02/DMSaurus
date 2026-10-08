from alembic import command
from alembic.config import Config

from src.config import BASE, DOCUMENT_PATH, DATA_PATH, DATABASE_URL
from src.dms.storage.filesystem import FileStorage


class Initializer:
    def __init__(self):
        self.document_dir = DOCUMENT_PATH
        self.data_dir = DATA_PATH

    def initialize(self):
        self._create_directories()
        self._init_filesystem()
        self._init_database()

    def _create_directories(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _init_filesystem(self):
        FileStorage(self.document_dir)

    def _init_database(self):
        alembic_config = Config(str(BASE / "alembic.ini"))

        alembic_config.set_main_option("sqlalchemy.url", DATABASE_URL)
        command.upgrade(alembic_config, "head")
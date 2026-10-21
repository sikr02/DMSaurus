import json
from sqlalchemy.orm import Session

from src.dms.database.models import ConfigEntry


class ConfigManager:
    def __init__(self, session: Session):
        self.session = session
        self._values = {}
        self.reload()

    def reload(self):
        with self.session as session:
            rows = session.query(ConfigEntry).all()
            self._values = {row.key: json.loads(row.value) for row in rows}

    def get(self, key, default=None):
        return self._values.get(key, default)

    def set(self, key, value):
        value_str = json.dumps(value)
        with self.session as session:
            entry = session.get(ConfigEntry, key)
            if entry is None:
                entry = ConfigEntry(key=key, value=value_str)
                session.add(entry)
            else:
                entry.value = value_str

            session.commit()
        self._values[key] = value
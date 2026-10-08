from pathlib import Path
import shutil


class FileStorage:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, source: Path, filename: str) -> Path:
        destination = self.root / filename
        shutil.copy2(source, destination)
        return destination

    def get(self, filename: str) -> Path:
        return self.root / filename

    def delete(self, filename: str) -> None:
        path = self.root / filename
        if path.exists():
            path.unlink()
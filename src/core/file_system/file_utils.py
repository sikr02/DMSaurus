from pathlib import Path


def number_of_elements(path: Path) -> tuple[int, int, int]:
    folders, files = _number_of_elements_recursive(path)
    return folders + files, folders, files

def _number_of_elements_recursive(path: Path):
    if path.is_file():
        return 0, 1
    elif path.is_dir():
        fo, fi = 1, 0
        elements = list(path.iterdir())
        for i in elements:
            folders, files = _number_of_elements_recursive(i)
            fo += folders
            fi += files
        return fo, fi
    else:
        return 0, 0

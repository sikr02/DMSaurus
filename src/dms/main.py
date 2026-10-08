import typer

from src.config import get_session, DOCUMENT_PATH
from src.dms.folders.service import FolderService
from src.dms.initializer.initializer import Initializer
from src.dms.storage.filesystem import FileStorage

app = typer.Typer(
    name="dms",
    no_args_is_help=True,
)

doc_app = typer.Typer()
folder_app = typer.Typer()
tag_app = typer.Typer()

app.add_typer(doc_app, name="document")
app.add_typer(folder_app, name="folder")
app.add_typer(tag_app, name="tag")


@app.callback()
def main_callback() -> None:
    """DMSaurus – Local Data Management System"""


@app.command()
def init() -> None:
    """Initialize DMS"""
    typer.echo("Initialize DMS...")

    initializer = Initializer()
    initializer.initialize()

    typer.echo("DMS initialized successfully.")


@folder_app.command()
def create(name: str) -> None:
    """Create a folder"""
    with get_session() as session:
        storage = FileStorage(DOCUMENT_PATH)
        service = FolderService(session, storage)
        folder = service.create_folder(name)

        typer.echo(
            f"Folder '{folder.name}' created (ID: {folder.id})."
        )


@folder_app.command()
def delete(folder_id: int) -> None:
    """Delete a folder by ID"""
    with get_session() as session:
        storage = FileStorage(DOCUMENT_PATH)
        service = FolderService(session, storage)
        success = service.delete_folder(folder_id)
        if success:
            typer.echo(f"Folder with ID {folder_id} deleted.")
        else:
            typer.echo(f"Folder with ID {folder_id} does not exist.")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
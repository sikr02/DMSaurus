from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


document_tags = Table(
    "document_tags",
    Base.metadata,
    Column(
        "document_id",
        ForeignKey("documents.id"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        ForeignKey("tags.id"),
        primary_key=True,
    )
)


class Folder(Base):
    __tablename__ = "folders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    parent_id: Mapped[int] = mapped_column(ForeignKey("folders.id"), nullable=True)
    parent: Mapped["Folder | None"] = relationship("Folder", remote_side="Folder.id", back_populates="children")
    children: Mapped[list["Folder"]] = relationship("Folder", back_populates="parent")

    documents: Mapped[list["Document"]] = relationship(back_populates="folder")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))

    stored_filename: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    folder_id: Mapped[int | None] = mapped_column(ForeignKey("folders.id"))

    folder: Mapped["Folder | None"] = relationship(back_populates="documents")

    tags: Mapped[list["Tag"]] = relationship(secondary=document_tags, back_populates="documents")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    documents: Mapped[list["Document"]] = relationship(secondary=document_tags, back_populates="tags")
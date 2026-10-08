from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dms.database.models import Tag


class TagService:
    def __init__(self, session: Session):
        # Link to database
        self.session = session

    def create_tag(self, name: str) -> Tag:
        existing_tag = self.get_tag_by_name(name)
        if existing_tag is not None:
            raise ValueError(f"Tag already exists: {name}")

        tag = Tag(name=name)
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def delete_tag(self, tag_id: int) -> bool:
        # Retrieve tag object from database
        tag = self.get_tag(tag_id)
        # If no tag with the ID exists, delete fails
        if tag is None:
            return False
        # Delete database entry
        self.session.delete(tag)
        self.session.commit()
        return True

    def get_tag(self, tag_id: int) -> Tag | None:
        return self.session.get(Tag, tag_id)

    def get_tag_by_name(self, name: str) -> Tag | None:
        statement = select(Tag).where(Tag.name == name)
        return self.session.scalar(statement)

    def list_tags(self) -> list[Tag]:
        statement = select(Tag)
        return list(self.session.scalars(statement).all())

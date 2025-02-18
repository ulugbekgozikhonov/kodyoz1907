from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModel
from app.models.problem_tag import problem_tag_association


class Tag(BaseModel):
	__tablename__ = "tags"

	name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	problems: Mapped[List["Problem"]] = relationship(
		secondary=problem_tag_association,
		back_populates="tags",
		lazy="selectin",
	)

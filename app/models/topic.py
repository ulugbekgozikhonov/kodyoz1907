from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.orm import Mapped, relationship

from app.db.base import BaseModel

problem_topic_association = Table(
	"problem_topic_association",
	BaseModel.metadata,
	Column("problem_id", ForeignKey("problems.id"), primary_key=True),
	Column("topic_id", ForeignKey("topics.id"), primary_key=True),
)


class Topic(BaseModel):
	__tablename__ = 'topics'

	problems: Mapped[list["Problem"]] = relationship(
		secondary=problem_topic_association,
		back_populates="topics",
		lazy="selectin",
	)

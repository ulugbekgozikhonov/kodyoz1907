import json

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModel
from app.models.topic import problem_topic_association, Topic


class Problem(BaseModel):
	__tablename__ = 'problems'

	title: Mapped[str] = mapped_column(String, nullable=False)
	level: Mapped[str] = mapped_column(String, nullable=False)
	hint: Mapped[str] = mapped_column(String, nullable=True)
	description: Mapped[str] = mapped_column(Text, nullable=False)
	constraints: Mapped[json] = mapped_column(JSON, nullable=True)

	submissions = relationship("Submission", back_populates="problem")
	test_cases = relationship("TestCase", back_populates="problem")
	topics: Mapped[list["Topic"]] = relationship(
		secondary=problem_topic_association,  # ✅ Many-to-Many bog‘lash
		back_populates="problems",
		lazy="selectin",  # ✅ Eager Loading - Performance uchun
	)

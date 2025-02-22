import enum

from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModel
from app.models.problem_tag import problem_tag_association


class Difficulty(enum.Enum):
	EASY = "Easy"
	MEDIUM = "Medium"
	HARD = "Hard"


class Problem(BaseModel):
	__tablename__ = 'problems'
	title: Mapped[str] = mapped_column(String(length=255), nullable=False)
	description: Mapped[str] = mapped_column(Text, nullable=False)
	hint: Mapped[str] = mapped_column(String(length=255), nullable=True)
	difficulty: Mapped[str] = mapped_column(Enum(Difficulty, name="difficulty_enum"), nullable=False)

	test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
	submissions = relationship("Submission", back_populates="problem")
	tags: Mapped[list["Tag"]] = relationship(
		secondary=problem_tag_association,
		back_populates="problems",
		lazy="selectin",
	)

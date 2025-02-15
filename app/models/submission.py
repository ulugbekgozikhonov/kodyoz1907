import enum
import uuid

from sqlalchemy import Enum, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.base import BaseModel


class SubmissionStatus(enum.Enum):
	PENDING = "Pending"
	ACCEPTED = "Accepted"
	WRONG_ANSWER = "Wrong Answer"
	TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"


class ProgrammingLanguage(enum.Enum):
	PYTHON = "Python"
	JAVA = "Java"
	CPP = "C++"
	JAVASCRIPT = "JavaScript"
	GO = "Go"


class Submission(BaseModel):
	__tablename__ = 'submissions'

	status: Mapped[SubmissionStatus] = mapped_column(Enum(SubmissionStatus, name="status_enum"), nullable=False)
	language: Mapped[ProgrammingLanguage] = mapped_column(Enum(ProgrammingLanguage, name="language_enum"),
	                                                      nullable=False, default=ProgrammingLanguage.PYTHON)
	runtime: Mapped[float] = mapped_column(Float, nullable=True)
	notes: Mapped[str] = mapped_column(Text, nullable=True)
	code: Mapped[str] = mapped_column(Text, nullable=False)
	problem_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('problems.id'), nullable=False)
	user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable=False)

	user = relationship("User", back_populates="submissions")
	problem = relationship("Problem", back_populates="submissions")

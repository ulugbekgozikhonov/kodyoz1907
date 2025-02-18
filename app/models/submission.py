import enum
import uuid

from sqlalchemy import Text, ForeignKey, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
	__tablename__ = "submissions"

	user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
	problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("problems.id"), nullable=False)
	code: Mapped[str] = mapped_column(Text, nullable=False)
	language: Mapped[str] = mapped_column(Enum(ProgrammingLanguage, name="language_enum"), nullable=False)
	status: Mapped[str] = mapped_column(Enum(SubmissionStatus, name="status_enum"), default="Pending")
	execution_time: Mapped[float] = mapped_column(Float, nullable=True)

	problem = relationship("Problem", back_populates="submissions")

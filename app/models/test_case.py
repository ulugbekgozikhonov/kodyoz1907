import uuid

from pydantic import BaseModel
from sqlalchemy import Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship


class TestCase(BaseModel):
	__tablename__ = 'test_cases'

	input: Mapped[str] = mapped_column(Text, nullable=False)
	output: Mapped[str] = mapped_column(Text, nullable=False)
	explanation: Mapped[str] = mapped_column(Text, nullable=True)
	problem_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('problems.id'), nullable=False)

	problem = relationship("Problems", back_populates="test_cases")

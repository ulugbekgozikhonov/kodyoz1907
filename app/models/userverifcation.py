import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel


class UserVerificationCode(BaseModel):
	__tablename__ = 'user_verification_code'
	user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	code: Mapped[str] = mapped_column(String, nullable=False)
	expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

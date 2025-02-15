import enum
from datetime import datetime

from sqlalchemy import String, Date, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModel


class UserRole(enum.Enum):
	ADMIN = "admin"
	USER = "user"


class User(BaseModel):
	__tablename__ = 'users'

	username: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
	firstname: Mapped[str] = mapped_column(String, nullable=False)
	lastname: Mapped[str] = mapped_column(String, nullable=False)
	email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
	password: Mapped[str] = mapped_column(String, nullable=False)
	gender: Mapped[str] = mapped_column(String, nullable=True)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True)
	role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="role_enum"), nullable=True, default=UserRole.USER)
	birth_date: Mapped[datetime] = mapped_column(Date, nullable=True)

	submissions = relationship("Submission", back_populates="user")

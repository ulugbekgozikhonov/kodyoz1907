import enum
from datetime import date

from sqlalchemy import String, Enum, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel


class GenderType(enum.Enum):
	MALE = 'male'
	FEMALE = 'female'


class User(BaseModel):
	__tablename__ = 'users'
	username: Mapped[str] = mapped_column(String(length=33), unique=True, nullable=False)
	firstname: Mapped[str] = mapped_column(String(length=50), nullable=True)
	lastname: Mapped[str] = mapped_column(String(length=50), nullable=True)
	photo_url: Mapped[str] = mapped_column(String(length=255), nullable=True)
	email: Mapped[str] = mapped_column(String(length=125), unique=True, nullable=False)
	password: Mapped[str] = mapped_column(String(length=255), nullable=False)
	gender: Mapped[GenderType] = mapped_column(Enum(GenderType, name="gender_enum"), nullable=True)
	is_active: Mapped[bool] = mapped_column(Boolean, default=False)
	birth_date: Mapped[date] = mapped_column(Date, nullable=True)

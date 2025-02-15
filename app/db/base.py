import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
	pass


class BaseModel(Base):
	__abstract__ = True
	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False, onupdate=func.now())

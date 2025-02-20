import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
	bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
	"""FastAPI uchun asinxron sessiya generatori."""
	async with async_session_maker() as session:
		yield session


dependency = Annotated[AsyncSession, Depends(get_db)]
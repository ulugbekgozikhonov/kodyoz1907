from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends

<<<<<<< HEAD

DATABASE_URL = os.getenv("DATABASE_URL")
=======
from app.core.config import settings
>>>>>>> e72a21ab618cf3b782abdc697a494139c10c3282

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
	bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
	"""FastAPI uchun asinxron sessiya generatori."""
	async with async_session_maker() as session:
		yield session


dependency = Annotated[AsyncSession, Depends(get_db)]
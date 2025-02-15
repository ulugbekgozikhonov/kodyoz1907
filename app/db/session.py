import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:root_123@localhost:5432/kodyoz1907")

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
	bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
	"""FastAPI uchun asinxron sessiya generatori."""
	async with async_session_maker() as session:
		yield session

import os

from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:root_123@localhost:5432/kodyoz1907")

engine = create_async_engine(DATABASE_URL, echo=True)

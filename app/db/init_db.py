import asyncio

from app.models.problem import BaseModel
from session import engine


async def init_db():
	"""📌 Database va barcha jadvallarni yaratish"""
	async with engine.begin() as conn:
		await conn.run_sync(BaseModel.metadata.create_all)

	print("✅ Database yaratildi!")


if __name__ == "__main__":
	asyncio.run(init_db())

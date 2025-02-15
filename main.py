from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User

app = FastAPI()


@app.get("/")
async def demo_user(db: AsyncSession = Depends(get_db)):
	user = User(
		username="devkhon",
		email="ketmon@gmail.com",
		password="asdfasdf",
		firstname="Asdfg",
		lastname="asdfgasdf",
		gender="male"
	)

	db.add(user)
	await db.commit()
	await db.refresh(user)
	return user

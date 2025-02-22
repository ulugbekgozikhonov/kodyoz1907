import random
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import exists
from sqlalchemy.future import select

from app.core.dependencies import db_dependency
from app.models import User, UserVerificationCode
from app.schemas.auth import UserCreate
from app.utils.email import send_verification_email

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter()


@router.post("/signup")
async def signup(user_create: UserCreate, db: db_dependency):
	if user_create.password != user_create.confirm_password:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Password mismatch",
		)
	query = select(exists().where(User.email == user_create.email))
	result = await db.execute(query)
	if result.scalar():
		raise HTTPException(
			status_code=400,
			detail="Email already registered")

	query = select(exists().where(User.username == user_create.username))
	result = await db.execute(query)
	if result.scalar():
		raise HTTPException(
			status_code=400,
			detail="Username already registered"
		)

	user = User(
		email=user_create.email,
		username=user_create.username,
		password=pwd_context.hash(user_create.password),
	)

	db.add(user)
	await db.commit()
	await db.refresh(user)

	user_verify = UserVerificationCode(
		user_id=user.id,
		code="".join([str(random.randint(0, 10)) for _ in range(6)]),
		expires_at=datetime.now() + timedelta(minutes=5),
	)

	db.add(user_verify)
	await db.commit()
	await db.refresh(user_verify)

	# await send_verification_email(user.email, user_verify.code)
	return {
		"success": True,
		"message": f"{user.email} send code {user_verify.code}",
	}

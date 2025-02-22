import random
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import exists
from sqlalchemy.future import select
from app.core.config import settings

from app.core.dependencies import db_dependency
from app.models import User, UserVerificationCode
from app.schemas.auth import UserCreate, UserLogin, UserLogin_Code
from app.utils.email import send_verification_email
from app.utils.create_token import create_access_token

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

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

	await send_verification_email(user.email, user_verify.code)
	return {
		"success": True,
		"message": f"{user.email} send code {user_verify.code}",
	}

@router.post("/login")
async def login(user_login: UserLogin, db: db_dependency):
    query = select(User).where(User.username == user_login.username) 
    result = await db.execute(query)
    user = result.scalars().first()

    if not user or not pwd_context.verify(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="Authentication failed")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"message": "Login successful", "token": access_token}


@router.post("/login_email_code")
async def login_email_code(user_login: UserLogin_Code, db: db_dependency):
    query = select(User).where(User.username == user_login.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user or not pwd_context.verify(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="Authentication failed")

    query = select(UserVerificationCode).where(
        UserVerificationCode.user_id == user.id
    ).order_by(UserVerificationCode.expires_at.desc())

    result = await db.execute(query)
    verification_code = result.scalars().first()

    if not verification_code:
        raise HTTPException(status_code=400, detail="Verification code not found")

    if not user_login.code:
        raise HTTPException(status_code=400, detail="Verification code is required")

    if verification_code.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code expired")

    if verification_code.code != user_login.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
	# if not verification_code or not user_login.code or verification_code.expires_at < datetime.utcnow() or verification_code.code != user_login.code:
    #     raise HTTPException(status_code=400, detail="Invalid, missing, or expired verification code")

    await db.delete(verification_code)
    await db.commit()

    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "message": "Login successful",
        "token": access_token
	}

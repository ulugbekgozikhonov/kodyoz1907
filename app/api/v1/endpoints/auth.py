import random
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import exists
from sqlalchemy.future import select

from app.core.dependencies import db_dependency
from app.models import User, UserVerificationCode
from app.schemas.auth import ForgetPassword, UserCreate, UserLogin, VerifyCode

# from app.utils.email import send_verification_email
from app.services.auth_service import generate_access_token, generate_code_verification


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        raise HTTPException(status_code=400, detail="Email already registered")

    query = select(exists().where(User.username == user_create.username))
    result = await db.execute(query)
    if result.scalar():
        raise HTTPException(status_code=400, detail="Username already registered")

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
        code=generate_code_verification(),
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


@router.post("/verify-code")
async def verify_code(verify_code: VerifyCode, db: db_dependency):
    query = select(User).where(User.email == verify_code.email)
    result = await db.execute(query)
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await db.execute(
        select(UserVerificationCode).where(
            UserVerificationCode.user_id == user.id,
            UserVerificationCode.code == verify_code.code,
        )
    )
    verification = result.scalars().first()

    if not verification:
        raise HTTPException(status_code=404, detail="Code not found")
    if verification.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="Code expired")
    token = await generate_access_token(user.id)
    return {"success": True, "message": "Code verified", "token": token}


@router.post("/login")
async def login(user_login: UserLogin, db: db_dependency):
    query = select(User).where(User.username == user_login.username)
    result = await db.execute(query)
    user = result.scalar()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(user_login.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    token = await generate_access_token(user.id)
    return {"success": True, "message": "Login successful", "token": token}


@router.post("/forgot-password")
async def forgot_password(forgot_password: ForgetPassword, db: db_dependency):
    query = select(User).where(User.username == forgot_password.username)
    result = await db.execute(query)
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_verify = UserVerificationCode(
        user_id=user.id,
        code=generate_code_verification(),
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


# @router.post("/reset-password")
# async def reset_password(verify_code: VerifyCode, db: db_dependency):

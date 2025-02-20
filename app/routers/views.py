# from fastapi import APIRouter
# from fastapi import APIRouter,HTTPException
# from .schemas import UserLogin, UserRegister
# from app.models import User
# from datetime import timedelta
# from datetime import datetime,timedelta
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from app.db.session import dependency
# import os

# SECRET_KEY= os.getenv("SECRET_KEY")
# ALGORITHM=os.getenv("ALGORITHM")

# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta 
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")



# router = APIRouter(tags=["customer"],prefix="/customer")

# @router.post("/register",status_code=201)
# async def login(user_req: UserRegister,db: dependency):
#     user = db.query(User).filter(User.name == user_req.name).first()
#     if user:
#         raise HTTPException(status_code=400,detail="Username already exists")
#     user = db.query(User).filter(User.email == user_req.email).first()
#     if user:
#         raise HTTPException(status_code=400,detail="Email already exists")
    
#     user = User(
#         data = user_req.data,
#         gender = user_req.gender,
#         username = user_req.username,
#         firstname = user_req.firstname,
#         lastname = user_req.lastname,
#         email = user_req.email,
#         photo_url = "image/image.png",
#         password = pwd_context.hash(user_req.password)
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     access_token = create_access_token(data={"sub":user.name},expires_delta=timedelta(minutes=30))

#     return {"user":user, "token":access_token}



# @router.post("/login")
# async def login(user_login: UserLogin,db: dependency):
#     user = db.query(User).filter(User.name == user_login.name).first()
#     if not user or not pwd_context.verify(user_login.password,user.password):
#         raise HTTPException(status_code=401,detail="Authentication failed")
#     access_token = create_access_token(data={"sub":user.name},expires_delta=timedelta(minutes=30))
    
#     return {"message":"Login successful", "token":access_token}


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserLogin, UserRegister
from app.models import User
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.db.session import dependency
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["customer"], prefix="/customer")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", status_code=201)
async def register(user_req: UserRegister, db: AsyncSession = Depends(dependency)):
    # Проверка существующего имени пользователя
    stmt = select(User).where(User.name == user_req.name)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Проверка существующего email
    stmt = select(User).where(User.email == user_req.email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Создание нового пользователя
    user = User(
        data=user_req.data,
        gender=user_req.gender,
        username=user_req.username,
        firstname=user_req.firstname,
        lastname=user_req.lastname,
        email=user_req.email,
        photo_url="image/image.png",
        password=pwd_context.hash(user_req.password),
    )

    db.add(user)
    await db.commit()  # Асинхронный коммит
    await db.refresh(user)  # Обновление объекта в сессии

    access_token = create_access_token(data={"sub": user.name}, expires_delta=timedelta(minutes=30))

    return {"user": user, "token": access_token}


@router.post("/login")
async def login(user_login: UserLogin, db: AsyncSession = Depends(dependency)):
    stmt = select(User).where(User.name == user_login.name)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user or not pwd_context.verify(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="Authentication failed")

    access_token = create_access_token(data={"sub": user.name}, expires_delta=timedelta(minutes=30))

    return {"message": "Login successful", "token": access_token}

from jose import jwt

from app.core.config import settings
from datetime import datetime, timedelta
import uuid
import random


async def generate_access_token(user_id: uuid.UUID) -> str:
    data = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)



# async def generate_refresh_token(user_id: uuid.UUID) -> str:
    # data = {
    #     "sub": str(user_id),
    #     "type": "refresh",
    #     "exp": datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    # }
    
    
    
async def generate_code_verification() -> str:
    return "".join([str(random.randint(0, 9)) for _ in range(6)])
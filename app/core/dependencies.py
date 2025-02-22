from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.db.session import get_db

db_dependency = Annotated[AsyncSession, Depends(get_db)]

from fastapi import FastAPI

from app.routers.views import router as user_router


app = FastAPI(title="KodYoz API", description="KodYoz api", version="1.0.0")


app.include_router(user_router, prefix="/user", tags=["user"])

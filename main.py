from fastapi import FastAPI
from app.api.v1.endpoints import auth




app = FastAPI(title="KodYoz API", description="KodYoz api", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])



from fastapi import FastAPI

from app.api.v1.endpoints import auth

app = FastAPI()

app.include_router(auth.router)


@app.get("/test")
async def root():
	return {"message": "Hello World"}

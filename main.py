from fastapi import FastAPI

<<<<<<< HEAD
from app.routers.views import router as user_router
=======
from app.api.v1.endpoints import auth

app = FastAPI()
>>>>>>> e72a21ab618cf3b782abdc697a494139c10c3282

app.include_router(auth.router)


<<<<<<< HEAD
app = FastAPI(title="KodYoz API", description="KodYoz api", version="1.0.0")


app.include_router(user_router, prefix="/user", tags=["user"])
=======
@app.get("/test")
async def root():
	return {"message": "Hello World"}
>>>>>>> e72a21ab618cf3b782abdc697a494139c10c3282

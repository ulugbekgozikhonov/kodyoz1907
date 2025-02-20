from pydantic import BaseModel, Field


class UserCreate(BaseModel):
	username: str = Field(min_length=3)
	password: str = Field(min_length=8)
	confirm_password: str = Field(min_length=8)
	email: str = Field(min_length=10)

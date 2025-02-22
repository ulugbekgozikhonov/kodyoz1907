from pydantic import BaseModel, Field


class UserCreate(BaseModel):
	username: str = Field(min_length=3)
	password: str = Field(min_length=8)
	confirm_password: str = Field(min_length=8)
	email: str = Field(min_length=10)

class VerifyCode(BaseModel):
	code: str = Field(min_length=6)
	email: str = Field(min_length=10)
 
 
 
class UserLogin(BaseModel):
	username: str = Field(min_length=3)
	password: str = Field(min_length=8)


class ForgetPassword(BaseModel):
	username: str = Field(min_length=3)
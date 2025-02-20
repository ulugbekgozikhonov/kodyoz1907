from pydantic import BaseModel, Field
    
class UserRegister(BaseModel):
    username: str = Field(min_length=3)
    firstname: str = Field(min_length=3)
    lastname: str = Field(min_length=3)
    email: str = Field(min_length=3)
    password: str = Field(min_length=3)
    data: str = Field(min_lenght=3)
    gender: str = Field(...)

class UserLogin(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3)
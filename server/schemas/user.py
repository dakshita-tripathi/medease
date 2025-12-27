from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    role: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserRegister(UserBase):
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    nickname: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int

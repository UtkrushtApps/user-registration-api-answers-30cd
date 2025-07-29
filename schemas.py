from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    password: constr(min_length=6, max_length=255)

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

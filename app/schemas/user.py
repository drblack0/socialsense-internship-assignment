from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    role: str = "user"


class UserInDBBase(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass

from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    name:str
    email:EmailStr
    password:str
    passwordConfirm:str
    role: Optional[str] = "user"


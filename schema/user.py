from .base_module import *
from datetime import datetime

class UserBase(BaseModel):
    cedula: str
    nombre: str
    apellido: str
    
class UserCreate(UserBase):
    email: EmailStr
    passwd:str
    
class User(UserBase):
    ingreso: datetime | None = None
    class Config:
        orm_mode=True
    
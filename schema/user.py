from .base_module import *
from datetime import datetime

class UserBase(BaseModel):
    cedula: str
    nombre: str
    apellido: str
    
class UserCreate(UserBase):
    email: EmailStr
    passwd:str
    
class UserToken(UserBase):
    token:str
    
    
class User(UserBase):
    ingreso: datetime | None = None
    is_actived: bool 
    class Config:
        orm_mode=True
    
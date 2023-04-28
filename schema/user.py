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
    is_actived: bool 
    
    class Config:
        orm_mode=True
    
    
#token schema
class TokenBase(BaseModel):
    access_token:str | None = None
      
class TokenCreate(TokenBase):
    user_cedula:str
    caducidad:datetime
      
class Token(TokenBase):
    token_type: str 
    
    class Config:
        orm_mode=True
        
    
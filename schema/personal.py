from .base_module import *
from .user import User
from enum import Enum

class permisos(Enum):
    read = 'r'
    write = 'rw'
    exec = 'rwx'
    all = 'drwx'

class PersonalBase(BaseModel):
    permisos: permisos
    
class PersonalCreate(PersonalBase):
    user_cedula: str

class Personal(PersonalBase):
    id: int 
    user: User 
    
    class Config:
        orm_mode=True
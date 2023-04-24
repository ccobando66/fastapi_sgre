from .base_module import *
from .user import User
from enum import Enum

class permisos(Enum):
    read = 'r'
    write = 'rw'
    exec = 'rwx'
    all = 'drwx'

class AdminBase(BaseModel):
    permisos: permisos
    
class AdminCreate(AdminBase):
    user_cedula: str

class Admin(AdminBase):
    id: int
    user: User
    
    class Config:
        orm_mode=True
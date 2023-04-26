from .base_module import *
from .user import User


class AdminBase(BaseModel):
    pass
    
class AdminCreate(AdminBase):
    user_cedula: str

class Admin(AdminBase):
    id: int
    user: User
    
    class Config:
        orm_mode=True
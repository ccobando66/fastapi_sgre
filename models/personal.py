from  models.base_module import *
from  models.user import Base
from  models.user import User

class Personal(Base):
    __tablename__ = 'personal'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    
    permisos = Column(
        String(4)
    )
    
    user_cedula = Column(
        String(11),
        ForeignKey('user.cedula')
    )
    
    user = relationship(
        'User',
         cascade='all, delete'
    )
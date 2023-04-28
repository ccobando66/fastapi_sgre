from .base_module import *
from ..config.database import Base


class User(Base):
    __tablename__ = 'user'
    cedula = Column(
        String(11),
        primary_key=True,
        index=True,
        
    )
    
    nombre = Column(
        String(100),
        
    )
    
    apellido = Column(
        String(100),
         
    )
    
    email = Column(
        String(200),
        index=True,
        unique=True  
    )
    
    passwd = Column(
        String
    )
    
    ingreso = Column(
        DateTime
    )
    
    is_actived = Column(
        Boolean,
        default=False
    )
    
    is_super_user = Column(
        Boolean,
        default=False
    )



class TokenUser(Base):
    __tablename__ = "token_user"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    access_token = Column(
        Text,
    )
    
    token_type = Column(
        String,
        default="bearer"
    )
    
    caducidad = Column(
        DateTime
    )
    
    user_cedula = Column(
        String(11),
        ForeignKey('user.cedula')
    )
    
    user = relationship(
        'User'
    )
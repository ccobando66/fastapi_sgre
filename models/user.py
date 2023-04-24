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
    
    is_super_user = Column(
        Boolean,
        default=False
    )
    
    
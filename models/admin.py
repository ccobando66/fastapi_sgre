from models.base_module import *
from models.personal import Base
from models.user import User

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
      
    user_cedula = Column(
        String(11),
        ForeignKey('user.cedula')
    )
    
    user = relationship(
        'User',
        cascade="all, delete"
    )
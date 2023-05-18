from .base_module import *
from .configuracion import Base



class Ubicacion(Base):
    __tablename__ = "ubicacion"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    direccion = Column(
        String,
        unique=True
    )
    
    ciudad = Column(
        String
    )
    
    sede = Column(
        String
    )
    

class Rack(Base):
    __tablename__ = "rack"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    nombre = Column(
        String
    )
    
    area = Column(
        String
    )
    
    piso = Column(
        String
    )
    
    disponible = Column(
        Boolean,
        default=True
    )
    
    ubicacion_id = Column(
        Integer,
        ForeignKey('ubicacion.id', ondelete='set null')
    )
    
    #many to one
    ubicacion = relationship(
        'Ubicacion'
    )
    
    
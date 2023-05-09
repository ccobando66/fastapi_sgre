from .base_module import *
from .equipo import Base


class Configuracion(Base):
    __tablename__ = "configuracion"
    
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    mombre = Column(
        String
    )
    
    ubicacion = Column(
        String
    )
    
    version = Column(
        Integer
    )
    
    estado = Column(
        String
    )
    
    creado = Column(
        DateTime,
        default=datetime.now()
    )
    
    eliminado = Column(
        DateTime
    )
    
    equipo_serial = Column(
        String,
        ForeignKey("equipo.serial")
    )
    
    equipo = relationship(
        'Equipo'
    )
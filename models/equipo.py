from .base_module import *
from ..models.admin import Base


class Equipo(Base):
    __tablename__ = 'equipo'

    serial = Column(
        String,
        primary_key=True,
        index=True
    )

    ingreso = Column(
        DateTime,
        default=datetime.now()
    )

    retiro = Column(
        DateTime

    )

    estado = Column(
        String
    )

    info_equipo_id = Column(
        Integer,
        ForeignKey('info_equipo.id')
    )

    personal_id = Column(
        Integer,
        ForeignKey('personal.id')
    )
    
    rack_id = Column(
        Integer,
        ForeignKey('rack.id')
    )

    # many to one
    info_equipo = relationship(
        'InfoEquipo'
    )

    # many to one
    personal = relationship(
        'Personal'
    )
    
    # many to one
    rack = relationship(
        'Rack'
    )


class TipoEquipo(Base):
    __tablename__ = 'tipo_equipo'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    host = Column(
        String,
        unique=True,
        index=True
    )

    port = Column(
        String(6)
    )

    username = Column(
        String(100)
    )

    password = Column(
        Text
    )

    device_type = Column(
        String
    )

    equipo_serial = Column(
        String,
        ForeignKey('equipo.serial', ondelete='set null')
    )

    equipo = relationship(
        'Equipo'
    )


class InfoEquipo(Base):
    __tablename__ = 'info_equipo'
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    modelo = Column(
        String
    )

    marca = Column(
        String
    )

    device = Column(
        String
    )

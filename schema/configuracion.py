from datetime import datetime

from .base_module import BaseModel, Enum
from .equipo import Equipo


class Estado(Enum):
    nuevo = "Nuevo"
    enviado = "Enviado"
    aplicado = "Aplicado"
    eliminado = "Eliminado"


class ConfiguracionBase(BaseModel):
    mombre: str
    version: int


class ConfiguracionCreate(ConfiguracionBase):
    estado: Estado
    equipo_serial: str


class Configuracion(ConfiguracionBase):
    equipo: Equipo

    class Config:
        orm_mode = True

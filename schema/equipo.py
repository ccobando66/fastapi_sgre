from .base_module import(
    BaseModel,List,Enum
)

from uuid import uuid4

from .personal import Personal

class Device(Enum):
    router = 'router'
    switch = 'switch'
    asa = 'asa'
    server = 'server'
    
class Estado(Enum):
    operativo = 'funcionando'
    nuevo  = 'sin configuracion'
    baja = "dado de baja"
    mantenimiento = "mantenimiento"
    novedad = "proceso de novedad"

class DeviceTipe(Enum):
    cisco_ios = "cisco_ios"
    cisco_asa = "cisco_asa"
    juniper_junos = "juniper_junos" 
    juniper = "juniper"
    f5_linux = "f5_linux"
    

class InfoEquipoBase(BaseModel):
    modelo: str
    marca: str
    device: Device

class InfoEquipo(InfoEquipoBase):
    id: int
    
    class Config:
        orm_mode=True 


class EquipoBase(BaseModel):
    serial:str = str(uuid4())
    estado : Estado = Estado.nuevo

class EquipoCreate(EquipoBase):
      info_equipo_id: int
      

class Equipo(EquipoBase):
      info_equipo: InfoEquipo | None = None
      
      class Config:
          orm_mode=True 
          

class TipoEquipoBase(BaseModel):
     host:str 
     port:str 

class TipoEquipoCreate(TipoEquipoBase):
    username:str
    password:str
    device_type:DeviceTipe
    equipo_serial:str | None
    
class TipoEquipo(TipoEquipoBase):
    id:int
    equipo:Equipo
    
    class Config:
        orm_mode=True


class EquipoPersona(BaseModel):
      id:int
      equipo:Equipo
      personal:Personal
      
      class Config:
          orm_mode=True
    
    
    


from .base_module import *


class UbicacionCreate(BaseModel):
     direccion:str
     ciudad:str 
     sede:str

class Ubicacion(UbicacionCreate):
    id:int
    
    class Config:
        orm_mode = True
    
    

class RackBase(BaseModel):
    nombre:str 
    area:str
    piso:str
    
class RackCreate(RackBase):
    ubicacion_id:int

class Rack(RackBase):
    id:int
    ubicacion:Ubicacion
    
    class Config:
        orm_mode = True
    

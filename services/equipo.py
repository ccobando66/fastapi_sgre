
from .base_module import *
from .crud_base import CrudBase

from ..models.equipo import (
    Equipo as EquipoModel,
    TipoEquipo as TipoEquipoModel,
    InfoEquipo as InfoEquipoModel 
)

from ..schema.equipo import (
    Equipo as EquipoSchema,EquipoCreate,
    TipoEquipo as TipoEquipoSchema,TipoEquipoCreate,
    InfoEquipoBase as InfoEquipoCreate, InfoEquipo as InfoEquipoSchema
)

from ..models.personal import Personal as PersonalModel
from passlib.hash import bcrypt




class Equipo(CrudBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
    
    
    def get_equipo(self, serial:str) -> EquipoModel:
        return super().get_model(EquipoModel,
                                 EquipoModel.serial,
                                 serial.strip())
    
    def get_personal(self, user_cedula:str) -> PersonalModel:
        return super().get_model(PersonalModel,
                                 PersonalModel.user_cedula,
                                 user_cedula.strip())
    
    def get_equipos(self,skip:int,limit:int) -> List[EquipoModel]:
        return super().get_many_models(EquipoModel,
                                       skip,
                                       limit)
    
    def create_equipo(self, equipo_schema:EquipoCreate, user_cedula:str) -> str | EquipoModel:
        personal_data = super().verify_data(data=user_cedula,
                                            fun_1=self.get_personal)
        
        if type(personal_data) == str:
            return personal_data
        
        if personal_data.permisos != 'drwx':
            return "requere permisos para realizar esta accion"
        
        equipo_schema.estado = equipo_schema.estado.value
        
        super().create_model(EquipoModel,
                             equipo_schema.dict())
        
        get_equipo = self.get_equipo(equipo_schema.serial)
        get_equipo.personal.append(personal_data)
        personal_data.equipo.append(get_equipo)
        super().get_session.commit()
        
        return get_equipo
    
    def create_info_equipo(self, info_equipo_schema:InfoEquipoCreate, user_cedula:str) -> InfoEquipoModel:
        personal_data = super().verify_data(data=user_cedula,
                                            fun_1=self.get_personal)
        
        if type(personal_data) == str:
            return personal_data
        
        if personal_data.permisos != 'drwx':
            return "requiere permisos para realizar esta accion"
        
        info_equipo_schema.device = info_equipo_schema.device.value
        
        super().create_model(InfoEquipoModel,
                             info_equipo_schema.dict())
        
        return super().get_session.query(InfoEquipoModel
                                         ).order_by(InfoEquipoModel.id.desc()
                                         ).first()
    
    def create_tipo_equipo(self, tipo_equipo_schema:TipoEquipoCreate, user_cedula:str) -> TipoEquipoModel:
        personal_data = super().verify_data(data=user_cedula,
                                            fun_1=self.get_personal)
        
        if super().get_model(TipoEquipoModel,
                             TipoEquipoModel.equipo_serial,
                             tipo_equipo_schema.equipo_serial.strip()):
           return f"{tipo_equipo_schema.equipo_serial} ya esta registrado en el sistema"
        
        if type(personal_data) == str:
            return personal_data
        
        if personal_data.permisos != 'drwx':
            return "requiere permisos para realizar esta accion"
        
        tipo_equipo_schema.device_type = tipo_equipo_schema.device_type.value
        tipo_equipo_schema.password = bcrypt.hash(tipo_equipo_schema.password.strip())
        
        super().create_model(TipoEquipoModel,
                             tipo_equipo_schema.dict())
        
        return super().get_session.query(TipoEquipoModel
                                         ).order_by(TipoEquipoModel.id.desc()
                                         ).first()
        
    def update_tipo_equipo(self, tipo_equipo_schema:TipoEquipoCreate, user_cedula:str) -> EquipoModel:
        
        tipo_equipo_data = super().get_model(TipoEquipoModel,
                                             TipoEquipoModel.host,
                                             tipo_equipo_schema.host.strip())
        
        if tipo_equipo_data is None:
            return f"{tipo_equipo_schema.host} no esta registrado en el sistema"
        
        personal_data = super().verify_data(data=user_cedula,
                                            fun_1=self.get_personal)
        if type(personal_data) == str:
            return personal_data
        
        if personal_data.permisos != 'drwx':
            return "requiere permisos para realizar esta accion"
        
        if tipo_equipo_schema.password is not None:
           tipo_equipo_schema.password = bcrypt.hash(tipo_equipo_schema.password.strip())
        
        if tipo_equipo_schema.device_type is not None:
           tipo_equipo_schema.device_type = tipo_equipo_schema.device_type.value 
           
        super().update_model(TipoEquipoModel,
                             TipoEquipoModel.host,
                             tipo_equipo_schema.host.strip(),
                             tipo_equipo_schema.dict(exclude_unset=True,
                                                     exclude={'host','equipo_serial'})
                             )
        
        return tipo_equipo_data

        
        
         
            
        
        
    
         
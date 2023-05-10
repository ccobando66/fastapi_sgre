from .base_module import Session
from .base_module import *
from .crud_base import CrudBase

from ..models.configuracion import Configuracion as ConfiguracionModel
from ..models.equipo import Equipo as EquipoModel, TipoEquipo as TipoEquipoModel

from ..schema.configuracion import (
    ConfiguracionCreate, Configuracion as ConfiguracionSchema
)

import aiofiles
from fastapi import UploadFile
import os
from passlib.hash import bcrypt
from netmiko import ConnectHandler


class Configuracion(CrudBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
    
    
    def get_configuracion(self, data:Any ) -> ConfiguracionModel:
        
        query_model = lambda my_data: ConfiguracionModel.id if type(my_data) == int else ConfiguracionModel.equipo_serial  
        return super().get_model(ConfiguracionModel,
                                 query_model(data),
                                 data)
        
    def get_personal(self, user_cedula:str) -> PersonalModel:
        return super().get_session.query(PersonalModel
                                         ).filter(PersonalModel.user_cedula == user_cedula
                                         ).first()
                                         
    
    def get_equipo(self, serial:str) -> EquipoModel:
        return super().get_model(EquipoModel,
                                 EquipoModel.serial,
                                 serial.strip())
    
    
    def create_configuracion(self,config_schema:ConfiguracionCreate) -> str | ConfiguracionModel:
        get_equipo = super().verify_data(data=config_schema.equipo_serial.strip(),
                                         fun_1=self.get_equipo
                                        )
        
        get_config = self.get_configuracion(config_schema.equipo_serial.strip())
        
        if type(get_equipo) == str:
            return get_equipo
        
        if get_config is not None:
            return "el equipo ya cuenta con configuracion"
        
        config_schema.equipo_serial = get_equipo.serial
        config_schema.estado = config_schema.estado.value
        
        super().create_model(ConfiguracionModel,
                             config_schema.dict())
        
        get_config = super().get_session.query(ConfiguracionModel
                                              ).order_by(ConfiguracionModel.id.desc()
                                              ).first()
                                              
        
        get_config.equipo = get_equipo
        super().get_session.commit() 
        
        return get_config
    
    async def create_file(self, file:UploadFile, datas:any) -> str | None:
                 
         file_path = f"{os.getcwd()}/sgre_v1/files/{file.filename}"
         get_config = super().verify_data(data=datas,
                                          fun_1=self.get_configuracion)
         
         if type(get_config) == str:
            return get_config 
         
         if file.content_type != 'text/plain':
            return f"{file.content_type} formato no valido" 
         
         if not os.path.exists(file_path):
            async with aiofiles.open(f"{file_path}","wb") as create_file:
                  out_file = await file.read()
                  await create_file.write(out_file)
            
         if get_config.ubicacion is None:
             get_config.ubicacion = f"/sgre_v1/files/{file.filename}"
             super().get_session.commit()
    
    def read_file_on_client(self,id:int) -> str:
        
        get_config = super().verify_data(data=id,
                                         fun_1=self.get_configuracion)
         
        if type(get_config) == str:
            return get_config 
        
        return f"{os.getcwd()}{get_config.ubicacion}"
    
    
    def send_config_on_device(self, passwd:str,serial:str) -> str | bool:
        get_connect = super().get_session.query(TipoEquipoModel.device_type,
                                                TipoEquipoModel.host,
                                                TipoEquipoModel.username,
                                                TipoEquipoModel.password,
                                                ).filter(TipoEquipoModel.equipo_serial == serial
                                                ).first()
        
        if get_connect is None or bcrypt.verify(passwd.strip(), get_connect.password) == False:
           return "Error!! contraseña o serial erroneos"
        
        my_device = get_connect._asdict() 
        my_device.update({'password':passwd.strip()})
        
        get_config = super().get_model(ConfiguracionModel,
                                       ConfiguracionModel.equipo_serial,
                                       serial)
        
        try:
            with ConnectHandler(**my_device) as net_connect:
                net_connect.send_config_from_file(f'{os.getcwd()}{get_config.ubicacion}')
                net_connect.save_config()
            return True 
        except Exception as ex:
               return  {'error':str(ex).split('\n')} 
        
    
    
         
         
             
         
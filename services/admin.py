from .crud_base import *

from ..schema.admin import AdminCreate, Admin as AdminSchema
from ..models.admin import Admin as AdminModel
from ..models.user import User as UserModel 
from ..models.personal import Personal as PersonalModel
from .crud_base import CrudBase


class Admin(CrudBase):
    
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        
    def get_user_by_admin(self,cedula:str) -> UserModel:
        return super().get_model(UserModel,
                          UserModel.cedula,
                          cedula
                          )
        
    def get_persona_by_admin(self,cedula:str) -> PersonalModel:
        return super().get_model(PersonalModel,
                          PersonalModel.user_cedula,
                          cedula)
        
    def get_admin(self,cedula:str) -> AdminModel:
        return super().get_model(AdminModel,
                          AdminModel.user_cedula,
                          cedula
                          )
        
    def get_admins(self,skip: int, limit: int) -> List[AdminModel]:
        return super().get_many_models(AdminModel, 
                                       skip, 
                                       limit)
    
    def create_admins(self,admin_schema:AdminCreate) -> str | AdminModel:
        get_user = super().verify_data(data=admin_schema.user_cedula,
                                       fun_1=self.get_user_by_admin,
                                       fun_2=self.get_persona_by_admin,
                                       fun_3=self.get_admin
                                      )
        if type(get_user) == str:
            return get_user
        
        
        if not get_user.is_super_user :
            return f"{admin_schema.user_cedula} no esta habilitado como administrador"
        
       
        admin_schema.user_cedula = get_user.cedula
        
        
        super().create_model(AdminModel,
                             admin_schema.dict()
                             )
        
        get_admin = self.get_admin(admin_schema.user_cedula)
        get_admin.user = get_user
        super().get_session.commit()
        
        return get_admin
    
    def delete_admin(self,cedula:str) -> AdminModel | str:
        try:
            user_db = self.get_admin(cedula)
            super().delete_model(user_db)
            return user_db
               
        except Exception:
            super().get_session.close()
            return f"{cedula} no existe en la base de datos" 
        
    #admin functions
    
    #helpers
    
    def get_user_and_status(self,cedula:str) -> str | Any:
        get_user = super().verify_data(data=cedula.strip(),
                                       fun_1=self.get_user_by_admin
                                       )
        
        if type(get_user) == str:
            return get_user
        
        return (get_user,get_user.is_actived)
        
    
    #functions
    def bloquear_user(self, cedula:str) -> str | UserModel:
        get_user = self.get_user_and_status(cedula)
        
        if type(get_user) == str:
            return get_user
        
        if get_user[1] == True:
            return f"{cedula} ya esta activo en el sistema"
        else:
            get_user[0].is_actived == True
            
        return get_user[0]
    
    def desbloquear_user(self, cedula:str) -> str | UserModel:
        get_user = self.get_user_and_status(cedula)
        
        if type(get_user) == str:
            return get_user
        
        if get_user[1] == False:
            return f"{cedula} perviamente esta bloqueado en el sistema"
        else:
            get_user[0].is_actived == False
        
        return get_user[0]
        
    
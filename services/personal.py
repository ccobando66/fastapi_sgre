from .base_module import *
from ..models.user import User as UserModel
from ..models.personal import Personal as PersonalModel
from ..schema.personal import Personal as PersonalShema, PersonalCreate
from .crud_base import CrudBase


class Personal(CrudBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        
    def get_personal(self,cedula: str) -> PersonalModel | None:
        return super().get_model(PersonalModel,
                                 PersonalModel.user_cedula,
                                 cedula)
    
    def get_personal_by_user(self,cedula: str) -> UserModel | None:
        return super().get_model(UserModel,
                                 UserModel.cedula,
                                 cedula
                                 ) 
                                        
    def get_personas(self,skip:int, limit: int) -> List[PersonalModel]:
        return super().get_many_models(PersonalModel,
                                       skip,
                                       limit
                                       )
    
    def create_personal(self,personal_schema:PersonalCreate) -> PersonalModel | str:
        
        get_user = self.get_personal_by_user(personal_schema.user_cedula.strip())
        if get_user is None:
            return f"{personal_schema.user_cedula} n esta registrado en el sistema" 
        
         
        if self.get_personal(personal_schema.user_cedula) is not None:
            return f"{personal_schema.user_cedula} ya esta registrado en el sistema" 
            
        personal_schema.user_cedula = get_user.cedula
        personal_schema.permisos = personal_schema.permisos.value    
        super().create_model(PersonalModel,
                             personal_schema.dict()
                            )
        get_personal = self.get_personal(personal_schema.user_cedula)
        get_personal.user = get_user
        super().get_session.commit()
            
        return self.get_personal(personal_schema.user_cedula)
        
        
        
    
    """"
    def update_personal(self,user_schema:UserCreate) -> PersonalModel | str:
        try:
            
            if user_schema.passwd is not None:
               user_schema.passwd = bcrypt.hash(user_schema.passwd.strip())
            
            super().update_model(PersonalModel,
                                 PersonalModel.cedula,
                                 user_schema.cedula.strip(),
                                 user_schema.dict(exclude_unset=True,
                                                  exclude={'cedula'}
                                                  )
                                )
            return self.get_user(user_schema.cedula)
        
        except Exception:
            super().get_session.close()
            return "A ocurrido un error, por favor verifique los datos"
    """
    def delete_personal(self,cedula:str) -> PersonalModel | str:
        try:
            user_db = self.get_personal(cedula.strip())
            super().delete_model(user_db)
            return user_db
               
        except Exception:
            super().get_session.close()
            return f"{cedula} no existe en la base de datos" 
       
        
        
        




from passlib.hash import bcrypt

from .base_module import *
from ..models.user import User as UserModel
from ..schema.user import User as UserShema, UserCreate
from .crud_base import CrudBase


class User(CrudBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
    
    def get_user(self,cedula: str) -> UserModel | None:
        return super().get_model(UserModel,
                                 UserModel.cedula,
                                 cedula.strip()
                                 )
    
    def get_users(self,skip:int, limit: int) -> List[UserModel]:
        return super().get_many_models(UserModel,
                                       skip,
                                       limit
                                       )
    
    def create_user(self,user_schema:UserCreate) -> UserModel | str:
        try:
            user_schema.passwd = bcrypt.hash(user_schema.passwd.strip())
            super().create_model(UserModel,
                                user_schema.dict()
                                )
            return self.get_user(user_schema.cedula)
        
        except Exception as ex:
            print(ex)
            super().get_session.close()
            return "A ocurrido un error, por favor verifique los datos"
        
    
    
    def update_user(self,user_schema:UserCreate) -> UserModel | str:
        try:
            
            if user_schema.passwd is not None:
               user_schema.passwd = bcrypt.hash(user_schema.passwd.strip())
            
            super().update_model(UserModel,
                                 UserModel.cedula,
                                 user_schema.cedula.strip(),
                                 user_schema.dict(exclude_unset=True,
                                                  exclude={'cedula'}
                                                  )
                                )
            return self.get_user(user_schema.cedula)
        
        except Exception:
            super().get_session.close()
            return "A ocurrido un error, por favor verifique los datos"
    
    def delete_user(self,cedula:str) -> UserModel | str:
        try:
            user_db = self.get_user(cedula.strip())
            super().delete_model(user_db)
            return user_db
               
        except Exception:
            super().get_session.close()
            return f"{cedula} no existe en la base de datos" 
        
        
     #funtion user
        
        




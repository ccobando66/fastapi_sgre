from datetime import datetime, timedelta
from os import getenv

from fastapi.encoders import jsonable_encoder
from passlib.hash import bcrypt

from ..auth.oauth2 import create_token
from ..models.admin import Admin as AdminModel
from ..models.user import TokenUser as TokenUserModel
from ..models.user import User as UserModel
from ..schema.user import Token as TokenSchema
from ..schema.user import TokenCreate
from ..schema.user import User as UserShema
from ..schema.user import UserCreate
from .base_module import *
from .crud_base import CrudBase


class User(CrudBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_user(self, cedula: str) -> UserModel | None:
        return super().get_model(UserModel,
                                 UserModel.cedula,
                                 cedula.strip()
                                 )

    def get_users(self, page: int, result_page: int) -> Tuple[List[UserModel],int]:
        skip = (page - 1) * result_page
        limit = skip + result_page
        return (super().get_many_models(UserModel,skip,limit),
                skip,
                limit)

    def create_user(self, user_schema: UserCreate) -> UserModel | str:
        try:
            user_schema.passwd = bcrypt.hash(user_schema.passwd.strip())
            super().create_model(UserModel,
                                 user_schema.dict(exclude_unset=True)
                                 )
            get_user = self.get_user(user_schema.cedula)
            if super().get_session.query(UserModel).count() == 1:
                get_user.is_actived = True
                get_user.is_super_user = True
                super().create_model(AdminModel,
                                     {'user_cedula': user_schema.cedula})
                super().get_session.commit()
            return get_user

        except Exception as ex:
            print(ex)
            super().get_session.close()
            return "A ocurrido un error, por favor verifique los datos"

    def update_user(self, user_schema: UserCreate) -> UserModel | str:
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

    def delete_user(self, cedula: str) -> UserModel | str:
        try:
            user_db = self.get_user(cedula.strip())
            super().delete_model(user_db)
            return user_db

        except Exception:
            super().get_session.close()
            return f"{cedula} no existe en la base de datos"

     # function user
    def login_user(self, username: str, passwd: str) -> str | TokenUserModel:
        get_user = super().get_model(UserModel,
                                     UserModel.email,
                                     username.strip()
                                     )

        if get_user is None or not bcrypt.verify(passwd, get_user.passwd):
            return "Usuario o contraseña errornea"

        get_token = super().get_model(TokenUserModel,
                                      TokenUserModel.user_cedula,
                                      get_user.cedula)

        expirate = datetime.now() + timedelta(minutes=int(getenv('JWT_EXPIRATE')))

        encode = TokenCreate(user_cedula=get_user.cedula,
                             caducidad=datetime.isoformat(expirate)
                             )

        get_user.ingreso = datetime.now()
        
        if get_token is None:
            
            token = create_token(jsonable_encoder(
                encode.dict(exclude={'access_token'})))
            if token is None:
                return "error al generar el token"
            encode.access_token = token

            super().get_session.commit()

            super().create_model(TokenUserModel,
                                 encode.dict()
                                 )

            generate_token = super().get_model(TokenUserModel,
                                               TokenUserModel.user_cedula,
                                               get_user.cedula
                                               )
            return generate_token

        elif datetime.now() >= get_token.caducidad:

            token = create_token(jsonable_encoder(
                encode.dict(exclude={'access_token'})))
            if token is None:
                return "error al generar el token"

            get_token.access_token = token
            get_token.caducidad = expirate
            super().get_session.commit()
            return get_token

        return get_token

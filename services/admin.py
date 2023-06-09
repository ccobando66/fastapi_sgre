from ..models.admin import Admin as AdminModel
from ..models.personal import Personal as PersonalModel
from ..models.user import User as UserModel
from ..schema.admin import Admin as AdminSchema
from ..schema.admin import AdminCreate
from .crud_base import *
from .crud_base import CrudBase


class Admin(CrudBase):

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_user_by_admin(self, cedula: str) -> UserModel:
        return super().get_model(UserModel,
                                 UserModel.cedula,
                                 cedula
                                 )

    def get_persona_by_admin(self, cedula: str) -> PersonalModel:
        return super().get_model(PersonalModel,
                                 PersonalModel.user_cedula,
                                 cedula)

    def get_admin(self, cedula: str) -> AdminModel:
        return super().get_model(AdminModel,
                                 AdminModel.user_cedula,
                                 cedula
                                 )

    def get_admins(self, skip: int, limit: int) -> List[AdminModel]:
        return super().get_many_models(AdminModel,
                                       skip,
                                       limit)

    def create_admins(self, admin_schema: AdminCreate) -> str | AdminModel:
        get_user = super().verify_data(data=admin_schema.user_cedula,
                                       fun_1=self.get_user_by_admin,
                                       fun_2=self.get_persona_by_admin,
                                       fun_3=self.get_admin
                                       )
        if type(get_user) == str:
            return get_user

        admin_schema.user_cedula = get_user.cedula

        super().create_model(AdminModel,
                             admin_schema.dict()
                             )

        get_admin = self.get_admin(admin_schema.user_cedula)
        get_admin.user = get_user
        get_user.is_super_user = True
        super().get_session.commit()

        return get_admin

    def delete_admin(self, cedula: str) -> AdminModel | str:
        try:
            user_db = self.get_admin(cedula)
            super().delete_model(user_db)
            return user_db

        except Exception:
            super().get_session.close()
            return f"{cedula} no existe en la base de datos"

    # admin functions

    # helpers

    def get_user_and_status(self, cedula: str) -> str | Tuple[UserModel,bool]:
        get_user = super().verify_data(data=cedula.strip(),
                                       fun_1=self.get_user_by_admin
                                       )

        if type(get_user) == str:
            return get_user

        return (get_user, get_user.is_actived)

    # functions
    def desbloquear_user(self, cedula: str) -> str | UserModel:
        get_user = self.get_user_and_status(cedula)

        if type(get_user) == str:
            return get_user

        if get_user[1] == True:
            return f"{cedula} ya esta activo en el sistema"
        else:
            get_user[0].is_actived = True
            super().get_session.commit()

        return get_user[0]

    def bloquear_user(self, cedula: str) -> str | UserModel:
        get_user = self.get_user_and_status(cedula)

        if type(get_user) == str:
            return get_user

        if get_user[1] == False:
            return f"{cedula} perviamente esta bloqueado en el sistema"
        else:
            get_user[0].is_actived = False
            super().get_session.commit()

        return get_user[0]

    def asignar_rol_super_usuario(self, cedula: str) -> str | UserModel:

        list_verify = [
            self.get_admin,
            self.get_user_by_admin
        ]

        for count, fun in enumerate(list_verify):
            data = super().verify_data(data=cedula,
                                       fun_1=fun
                                       )
            if type(data) == str:
                return data

            if len(list_verify) == count+1:
                list_verify.clear()
                list_verify.append(data)

        if list_verify[0].is_super_user:
            return f"{cedula} eres super usuario genial"
        else:
            list_verify[0].is_super_user = True
            super().get_session.commit()

        return list_verify[0]

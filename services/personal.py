from ..models.personal import Personal as PersonalModel
from ..models.user import User as UserModel
from ..schema.personal import Personal as PersonalShema
from ..schema.personal import PersonalCreate
from .base_module import *
from .crud_base import CrudBase


class Personal(CrudBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_personal(self, cedula: str) -> PersonalModel | None:
        return super().get_model(PersonalModel,
                                 PersonalModel.user_cedula,
                                 cedula)

    def get_personal_by_user(self, cedula: str) -> UserModel | None:
        return super().get_model(UserModel,
                                 UserModel.cedula,
                                 cedula
                                 )

    def get_personas(self, skip: int, limit: int) -> List[PersonalModel]:
        return super().get_many_models(PersonalModel,
                                       skip,
                                       limit
                                       )

    def create_personal(self, personal_schema: PersonalCreate) -> PersonalModel | str:

        get_user = super().verify_data(data=personal_schema.user_cedula,
                                       fun_1=self.get_personal_by_user,
                                       fun_2=self.get_personal
                                       )

        if type(get_user) == str:
            return get_user

        personal_schema.user_cedula = get_user.cedula
        personal_schema.permisos = personal_schema.permisos.value
        super().create_model(PersonalModel,
                             personal_schema.dict()
                             )
        get_personal = self.get_personal(personal_schema.user_cedula)
        get_personal.user = get_user
        super().get_session.commit()

        return self.get_personal(personal_schema.user_cedula)

    def update_personal(self, personal_schema: PersonalCreate) -> PersonalModel | str:

        result = super().verify_data(data=personal_schema.user_cedula,
                                     fun_1=self.get_personal
                                     )

        if type(result) == str:
            return result

        personal_schema.permisos = personal_schema.permisos.value
        super().update_model(PersonalModel,
                             PersonalModel.user_cedula,
                             personal_schema.user_cedula.strip(),
                             personal_schema.dict(exclude_unset=True,
                                                  exclude={'user_cedula'}
                                                  )
                             )
        return self.get_personal(personal_schema.user_cedula)

    def delete_personal(self, cedula: str) -> PersonalModel | str:
        try:
            user_db = self.get_personal(cedula.strip())
            super().delete_model(user_db)
            return user_db

        except Exception:
            super().get_session.close()
            return f"{cedula} no existe en la base de datos"

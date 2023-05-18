from ..models.personal import Personal as PersonalModel
from ..models.ubicacion import Rack as RackModel
from ..models.ubicacion import Ubicacion as UbicacionModel
from ..schema.ubicacion import Rack as RackSchema
from ..schema.ubicacion import RackCreate
from ..schema.ubicacion import Ubicacion as UbicacionSchema
from ..schema.ubicacion import UbicacionCreate
from .base_module import *
from .base_module import Session
from .crud_base import CrudBase


class Ubicacion(CrudBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_ubicacion(self, id: int) -> UbicacionModel:
        return super().get_model(UbicacionModel,
                                 UbicacionModel.id,
                                 id)

    def get_rack(self, id: int) -> RackModel:
        return super().get_model(RackModel,
                                 RackModel.id,
                                 id)

    def get_personal(self, cedula: str) -> PersonalModel:
        return super().get_model(PersonalModel,
                                 PersonalModel.user_cedula,
                                 cedula)

    def get_ubicaciones(self, page: int = 1, result_page: int = 10) -> Tuple[List[UbicacionSchema], int]:
        skip = (page - 1) * result_page
        limit = skip + result_page
        return (super().get_many_models(RackModel, skip, limit),
                skip,
                limit)

    def get_racks(self, page: int = 1, result_page: int = 10) -> Tuple[List[RackModel], int]:
        skip = (page - 1) * result_page
        limit = skip + result_page
        return (super().get_many_models(RackModel, skip, limit),
                skip,
                limit)

    def create_ubicacion(self, ubicacion_schema: UbicacionCreate, cedula: str) -> str | UbicacionModel:
        get_personal = super().verify_data(data=cedula,
                                           fun_1=self.get_personal)

        if type(get_personal) == str:
            return get_personal

        if get_personal.permisos != 'drwx':
            return f"requiere permisos para realizar esta accion"

        super().create_model(UbicacionModel,
                             ubicacion_schema.dict())

        get_ubicacion = super().get_session.query(UbicacionModel
                                                  ).order_by(UbicacionModel.id.desc()
                                                             ).first()

        return get_ubicacion

    def create_rack(self, rack_schema: RackCreate, cedula: str) -> str | RackModel:
        get_personal = super().verify_data(data=cedula,
                                           fun_1=self.get_personal)

        if type(get_personal) == str:
            return get_personal

        if get_personal.permisos != 'drwx':
            return f"requiere permisos para realizar esta accion"

        get_ubicacion = self.get_ubicacion(rack_schema.ubicacion_id)
        if get_ubicacion is None:
            return f"{rack_schema.ubicacion_id} no esta registrado en el sistema"

        super().create_model(RackModel,
                             rack_schema.dict())

        get_rack = super().get_session.query(RackModel
                                             ).order_by(RackModel.id.desc()
                                                        ).first()

        get_rack.ubicacion = get_ubicacion
        super().get_session.commit()

        return get_rack

    def update_ubicacion(self, id: int, ubicacion_schema: UbicacionCreate, cedula: str) -> str | UbicacionModel:
        get_personal = super().verify_data(data=cedula,
                                           fun_1=self.get_personal)

        if type(get_personal) == str:
            return get_personal

        if get_personal.permisos in ('r', 'rw'):
            return f"requiere permisos para realizar esta accion"

        if self.get_ubicacion(id) is None:
            return f"ubicacion con id= {id} no esta registrado en el sistema"

        super().update_model(UbicacionModel,
                             UbicacionModel.id,
                             id,
                             ubicacion_schema.dict())

        return self.get_ubicacion(id)

    def update_rack(self, id: int, rack_schema: RackSchema, cedula: str) -> str | RackModel:
        get_personal = super().verify_data(data=cedula,
                                           fun_1=self.get_personal)

        if type(get_personal) == str:
            return get_personal

        if get_personal.permisos in ('r', 'rw'):
            return f"requiere permisos para realizar esta accion"

        if self.get_rack(id) is None:
            return f"rack con id= {id} no esta registrado en el sistema"

        super().update_model(RackModel,
                             RackModel.id,
                             id,
                             rack_schema.dict())

        return self.get_rack(id)

    def delete_ubicacion(self, id: int, cedula: str) -> str | UbicacionModel:
        get_personal = super().verify_data(data=cedula,
                                           fun_1=self.get_personal)

        if type(get_personal) == str:
            return get_personal

        if get_personal.permisos in ('r', 'rw'):
            return "requiere permisos para realizar esta accion"

        get_ubicacion = self.get_ubicacion(id)

        if get_ubicacion is None:
            return f"ubicacion con id= {id} no esta registrado en el sistema"

        super().delete_model(get_ubicacion)

        return get_ubicacion

    def delete_rack(self, id: int, cedula: str) -> str | RackModel:
        get_personal = super().verify_data(data=cedula,
                                           fun_1=self.get_personal)

        if type(get_personal) == str:
            return get_personal

        if get_personal.permisos in ('r', 'rw'):
            return "requiere permisos para realizar esta accion"

        get_rack = self.get_rack(id)

        if get_rack is None:
            return f"rack con id= {id} no esta registrado en el sistema"

        super().delete_model(get_rack)

        return get_rack

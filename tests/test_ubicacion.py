import pytest

from ..services.ubicacion import RackCreate, Ubicacion, UbicacionCreate
from .base_module import *

session = TestSessionLocal()


class TestUbicacion:
    def test_create_ubicacion(self):
        session.rollback()
        data = self.service_ubicacion.create_ubicacion(TestUbicacion.create_data_ubicacion(),
                                                       '1012432366')
        assert type(data) != str
        assert data.ciudad == 'el vaticano'
        self.delete_and_reset_ubicacion(data)

    def test_get_ubicacion_success(self):
        session.rollback()
        self.service_ubicacion.create_ubicacion(TestUbicacion.create_data_ubicacion(),
                                                '1012432366')
        session.close()
        result = self.service_ubicacion.get_ubicacion(1)
        assert result != None
        assert result.direccion == 'calle troya 123'
        self.delete_and_reset_ubicacion(result)

    def test_create_rack(self):
        session.rollback()
        data_ubicacion = self.service_ubicacion.create_ubicacion(TestUbicacion.create_data_ubicacion(),
                                                                 '1012432366')
        session.close()

        data_rack = self.service_ubicacion.create_rack(TestUbicacion.create_data_rack(),
                                                       '1012432366')
        session.close()

        assert type(data_ubicacion) != str
        assert type(data_rack) != str
        assert data_rack.area == 'Cuarto de equipos'

        self.delete_and_reset_ubicacion(data_ubicacion)
        self.delete_and_reset_ubicacion(data_rack)

    def test_get_rack_sucess(self):
        session.rollback()
        data_ubicacion = self.service_ubicacion.create_ubicacion(TestUbicacion.create_data_ubicacion(),
                                                                 '1012432366')
        session.close()

        self.service_ubicacion.create_rack(TestUbicacion.create_data_rack(),
                                           '1012432366')
        session.close()

        result = self.service_ubicacion.get_rack(1)
        assert result != None
        assert result.nombre == 'Rack Gestion'

        self.delete_and_reset_ubicacion(data_ubicacion)
        self.delete_and_reset_ubicacion(result)

    def test_get_rack_failue(self):
        result = self.service_ubicacion.get_rack(1)
        assert result == None

    def test_get_ubicacion_failue(self):
        result = self.service_ubicacion.get_ubicacion(1)
        assert result == None

    @staticmethod
    def create_data_ubicacion() -> UbicacionCreate:
        return UbicacionCreate(direccion='calle troya 123',
                               ciudad='el vaticano',
                               sede='principal')

    @staticmethod
    def create_data_rack() -> RackCreate:
        return RackCreate(nombre='Rack Gestion',
                          area='Cuarto de equipos',
                          piso='A3',
                          ubicacion_id=1)

    @property
    def service_ubicacion(self) -> Ubicacion:
        return Ubicacion(session)

    def delete_and_reset_ubicacion(self, data: any) -> None:
        self.service_ubicacion.delete_model(data)
        session.close()

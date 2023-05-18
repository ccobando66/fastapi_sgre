import pytest

from ..config.database import SessionLocal
from ..services.ubicacion import RackCreate, Ubicacion, UbicacionCreate
from .base_module import *

session = SessionLocal()


class TestUbicacion:
    def test_create_ubicacion(self):

        data = self.set_data_ubicacion()
        assert type(data) != str
        assert data.ciudad == 'el vaticano'
        self.delete_and_reset_ubicacion(data)

    def test_get_ubicacion_success(self):

        self.set_data_ubicacion()
        result = self.service_ubicacion.get_ubicacion(1)
        assert result != None
        assert result.direccion == 'calle troya 123'
        self.delete_and_reset_ubicacion(result)

    def test_create_rack(self):

        data_ubicacion = self.set_data_ubicacion()
        data_rack = self.set_data_rack()
        assert type(data_ubicacion) != str
        assert type(data_rack) != str
        assert data_rack.area == 'Cuarto de equipos'
        self.delete_and_reset_ubicacion(data_ubicacion)
        self.delete_and_reset_ubicacion(data_rack)

    def test_get_rack_sucess(self):

        data_ubicacion = self.set_data_ubicacion()
        self.set_data_rack()
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

    def test_get_list_ubicacion(self):
        
        data_ubicacion = self.set_data_ubicacion()
        result = self.service_ubicacion.get_ubicaciones(0, 10)
        assert result != 0
        assert result[0].ciudad == 'el vaticano'
        self.delete_and_reset_ubicacion(data_ubicacion)
    
    def test_get_list_racks(self):
        
        data_ubicacion = self.set_data_ubicacion()
        self.set_data_rack()
        result = self.service_ubicacion.get_racks(0, 10)
        assert result != 0
        assert result[0].piso == 'A3'
        self.delete_and_reset_ubicacion(data_ubicacion)
        self.delete_and_reset_ubicacion(result[0])

    def test_update_ubicacion_success(self):

        data_ubicacion = self.set_data_ubicacion()
        update_data = UbicacionCreate(direccion='calle troya 123 avenida galapalos',
                                      ciudad='atenas',
                                      sede='atenas 2')
        result = self.service_ubicacion.update_ubicacion(
            1, update_data, '1012432367')
        assert type(result) != str
        assert result.ciudad == 'atenas'
        self.delete_and_reset_ubicacion(data_ubicacion)

    def test_update_ubicacion_failue_id(self):

        update_data = UbicacionCreate(direccion='calle troya 123 avenida galapalos',
                                      ciudad='atenas',
                                      sede='atenas 2')
        result = self.service_ubicacion.update_ubicacion(
            1, update_data, '1012432367')
        assert result == "ubicacion con id= 1 no esta registrado en el sistema"

    def test_update_ubicacion_failue_permisos(self):

        update_data = UbicacionCreate(direccion='calle troya 123 avenida galapalos',
                                      ciudad='atenas',
                                      sede='atenas 2')
        result = self.service_ubicacion.update_ubicacion(
            1, update_data, '1012432364')
        assert result == "requiere permisos para realizar esta accion"

    def test_update_rack_sucess(self):
        data_ubicacion = self.set_data_ubicacion()
        data_rack = self.set_data_rack()
        update_rack = RackCreate(nombre='Rack Border',
                                 area='ISP',
                                 piso='A3',
                                 ubicacion_id=1)

        result = self.service_ubicacion.update_rack(
            1, update_rack, '1012432367')
        assert type(result) != str
        assert result.area == 'ISP'
        assert result.id == 1

        self.delete_and_reset_ubicacion(data_ubicacion)
        self.delete_and_reset_ubicacion(data_rack)

    def test_delete_ubicacion_success(self):
        self.set_data_ubicacion()
        result = self.service_ubicacion.delete_ubicacion(1, '1012432367')
        assert type(result) != str
        assert result.direccion == 'calle troya 123'

    def test_delete_rack_success(self):
        data_ubicacion = self.set_data_ubicacion()
        self.set_data_rack()
        result = self.service_ubicacion.delete_rack(1, '1012432367')
        assert type(result) != str
        assert result.area == 'Cuarto de equipos'
        self.delete_and_reset_ubicacion(data_ubicacion)

    def __del__(self):
        session.rollback()

    @property
    def create_data_ubicacion(self) -> UbicacionCreate:
        return UbicacionCreate(direccion='calle troya 123',
                               ciudad='el vaticano',
                               sede='principal')

    @property
    def create_data_rack(self) -> RackCreate:
        return RackCreate(nombre='Rack Gestion',
                          area='Cuarto de equipos',
                          piso='A3',
                          ubicacion_id=1)

    @property
    def service_ubicacion(self) -> Ubicacion:
        return Ubicacion(session)

    def set_data_ubicacion(self):
        return self.service_ubicacion.create_ubicacion(self.create_data_ubicacion,
                                                       '1012432367')

    def set_data_rack(self):
        return self.service_ubicacion.create_rack(self.create_data_rack,
                                                  '1012432367')

    def delete_and_reset_ubicacion(self, data: any) -> None:
        self.service_ubicacion.delete_model(data)
        session.close()

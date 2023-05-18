from ..services.ubicacion import RackCreate, RackSchema
from ..services.ubicacion import Ubicacion as UbicacionService
from ..services.ubicacion import UbicacionCreate, UbicacionSchema
from .base_module import *


router = APIRouter(prefix='/ubicacion',
                   tags=['Ubicacion'],
                   dependencies=[Depends(is_personal_user)])


# ubicacion

@router.get('/{id}', response_model=UbicacionSchema)
async def read_ubicacion(id: int,
                         session: common_seccion):
    data = UbicacionService(session).get_ubicacion(id)
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{id} no esta registrado en el sistema"
        )

    return data


@router.get('/', response_model=Dict[str, List[UbicacionSchema] | Any])
async def read_ubicaciones(page: int,
                           max_page: int,
                           session: common_seccion):

    data = UbicacionService(session).get_ubicaciones(page)
    return {
        'data': data[0],
        'page': page,
        'start': data[1],
        'end': data[2],
        'total': max_page
    }


@router.post('/',
             response_model=UbicacionSchema,
             status_code=status.HTTP_201_CREATED)
async def set_ubicacion(ubcacion_schema: UbicacionCreate,
                        session: common_seccion,
                        cedula: Annotated[str, router.dependencies[0]]):

    data = UbicacionService(session).create_ubicacion(ubcacion_schema, cedula)
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data


@router.put('/{id}',
            response_model=UbicacionSchema)
async def modify_ubicacion(id: int,
                           ubcacion_schema: UbicacionCreate,
                           session: common_seccion,
                           cedula: Annotated[str, router.dependencies[0]]):

    data = UbicacionService(session).update_ubicacion(
        id, ubcacion_schema, cedula)
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data


@router.delete('/{id}',
               response_model=UbicacionSchema)
async def remove_ubicacion(id: int,
                           session: common_seccion,
                           cedula: Annotated[str, router.dependencies[0]]):

    data = UbicacionService(session).delete_ubicacion(id, cedula)
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data

# rack


@router.get('/rack/{id}', response_model=RackSchema)
async def read_rack(id: int,
                    session: common_seccion):
    data = UbicacionService(session).get_rack(id)
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{id} no esta registrado en el sistema"
        )

    return data


@router.get('/rack/', response_model=Dict[str, List[RackSchema] | Any])
async def read_racks(page: int,
                    max_page: int,
                    session: common_seccion):

    data = UbicacionService(session).get_racks(page, max_page)
    return {
        'data': data[0],
        'page': page,
        'start': data[1],
        'end': data[2],
        'total': max_page
    }


@router.post('/rack/',
             response_model=RackSchema,
             status_code=status.HTTP_201_CREATED)
async def set_rack(rack_schema: RackCreate,
                   session: common_seccion,
                   cedula: Annotated[str, router.dependencies[0]]):

    data = UbicacionService(session).create_rack(rack_schema, cedula)
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data


@router.put('/rack/{id}',
            response_model=RackSchema)
async def modify_rack(id: int,
                      rack_schema: RackCreate,
                      session: common_seccion,
                      cedula: Annotated[str, router.dependencies[0]]):

    data = UbicacionService(session).update_rack(id, rack_schema, cedula)
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data


@router.delete('/rack/{id}',
               response_model=RackSchema)
async def remove_rack(id: int,
                      session: common_seccion,
                      cedula: Annotated[str, router.dependencies[0]]):

    data = UbicacionService(session).delete_rack(id, cedula)
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data

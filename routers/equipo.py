from ..services.equipo import Equipo as EquipoService
from ..services.equipo import (EquipoCreate, EquipoSchema, InfoEquipoCreate,
                               InfoEquipoSchema, TipoEquipoCreate,
                               TipoEquipoSchema)
from .base_module import *

router = APIRouter(prefix='/equipo',
                   tags=['Equipo'],
                   dependencies=[Depends(get_valid_user),
                                 Depends(is_personal_user)]
                   )


@router.get('/{serial}', response_model=EquipoSchema)
async def read_equipo(serial: str, session: common_seccion):

    data = EquipoService(session).get_equipo(serial)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no existe registro en la base de datos"
        )
    return data


@router.get('/', response_model=Dict[str, List[EquipoSchema] | Any])
async def read_many_equipo(page: Annotated[int, Query(..., gt=0)],
                           max_page: Annotated[int, Query(..., ge=10)],
                           session: common_seccion,
                           user_data: Annotated[dict, router.dependencies[0]]):

    data = EquipoService(session).get_equipos_by_personal(page,
                                                          max_page)
    return {
        'data': data[0],
        'page': page,
        'start': data[1],
        'end': data[2],
        'total': max_page
    }


@router.post(path='/',
             response_model=EquipoSchema,
             status_code=status.HTTP_201_CREATED
             )
async def create_equipo(equipo_schema: EquipoCreate,
                        seccion: common_seccion,
                        user_data: Annotated[dict, router.dependencies[0]]):

    data = EquipoService(seccion).create_equipo(
        equipo_schema, user_data['cedula'])
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data


@router.post(path='/info',
             response_model=InfoEquipoSchema,
             status_code=status.HTTP_201_CREATED
             )
async def create_info_equipo(info_equipo_schema: InfoEquipoCreate,
                             seccion: common_seccion,
                             user_data: Annotated[dict, router.dependencies[0]]):

    data = EquipoService(seccion).create_info_equipo(
        info_equipo_schema, user_data['cedula'])
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data


@router.post(path='/tipo',
             response_model=TipoEquipoSchema,
             status_code=status.HTTP_201_CREATED
             )
async def create_tipo_equipo(info_equipo_schema: TipoEquipoCreate,
                             seccion: common_seccion,
                             user_data: Annotated[dict, router.dependencies[0]]):

    data = EquipoService(seccion).create_tipo_equipo(
        info_equipo_schema, user_data['cedula'])
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data


@router.patch(path='/tipo',
              response_model=TipoEquipoSchema,
              status_code=status.HTTP_201_CREATED
              )
async def alter_tipo_equipo(info_equipo_schema: TipoEquipoCreate,
                            seccion: common_seccion,
                            user_data: Annotated[dict, router.dependencies[0]]):

    data = EquipoService(seccion).update_tipo_equipo(
        info_equipo_schema, user_data['cedula'])
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data


@router.delete('/{serial}/eliminar',
               response_model=EquipoSchema | None,
               dependencies=[Depends(is_super_user)]
               )
async def delete_equipo(serial: str, seccion: common_seccion):
    data = EquipoService(seccion).deleted_equipo(serial)
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data

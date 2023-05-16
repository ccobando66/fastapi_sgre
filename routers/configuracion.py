from fastapi import File, Form, UploadFile
from fastapi.background import BackgroundTasks
from fastapi.responses import FileResponse

from ..services.configuracion import Configuracion as ConfiguracionService
from ..services.configuracion import ConfiguracionCreate, ConfiguracionSchema
from .base_module import *

router = APIRouter(prefix='/config',
                   tags=['Config'],
                   dependencies=[Depends(get_valid_user)]
                   )


@router.get('/{id}',
            response_model=ConfiguracionSchema
            )
async def read_config(id: int | str,
                      session: common_seccion,
                      user_data: Annotated[dict, router.dependencies[0]]):

    personal = ConfiguracionService(session).get_personal(user_data['cedula'])
    if personal.permisos is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="requiere permisos para realizar esta accion"
        )

    data = ConfiguracionService(session).get_configuracion(id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no existe registro en la base de datos"
        )
    return data


@router.get('/{id}/file',response_class=FileResponse)
async def read_file(id: int | str,
                    session: common_seccion,
                    user_data: Annotated[dict, router.dependencies[0]]):

    personal = ConfiguracionService(session).get_personal(user_data['cedula'])
    if personal.permisos is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="requiere permisos para realizar esta accion"
        )

    data = ConfiguracionService(session).read_file_on_client(id)
    if data.find('/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )

    return FileResponse(data)


@router.get('/{id}/download', response_class=FileResponse)
async def download_file(id: int | str,
                        session: common_seccion,
                        user_data: Annotated[dict, router.dependencies[0]]):

    personal = ConfiguracionService(session).get_personal(user_data['cedula'])
    if personal.permisos in [None, 'r', 'rw']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="requiere permisos para realizar esta accion"
        )
    data = ConfiguracionService(session).read_file_on_client(id)
    if data.find('/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )

    return FileResponse(data,
                        media_type="application/octet-stream",
                        filename=data.split('/')[-1])


@router.post('/',
             response_model=ConfiguracionSchema,
             response_model_exclude={'id'},
             status_code=status.HTTP_201_CREATED
             )
async def create_config(config_schema: ConfiguracionCreate,
                        session: common_seccion,
                        user_data: Annotated[dict, router.dependencies[0]]
                        ):

    personal = ConfiguracionService(session).get_personal(user_data['cedula'])
    if personal.permisos in [None, 'r', 'rw']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="requiere permisos para realizar esta accion"
        )

    data = ConfiguracionService(session).create_configuracion(config_schema)
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data


@router.post('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def create_file(file: Annotated[UploadFile, File()],
                      session: common_seccion,
                      id: int | str,
                      background_task: BackgroundTasks,
                      user_data: Annotated[dict, router.dependencies[0]]):

    personal = ConfiguracionService(session).get_personal(user_data['cedula'])
    if personal.permisos in [None, 'r', 'rw']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="requiere permisos para realizar esta accion"
        )

    background_task.add_task(await ConfiguracionService(session).create_file(file, id))
    return {'sms': 'peticion aceptada, se esta procesando'}


@router.post('/send/config',
             status_code=status.HTTP_202_ACCEPTED)
async def create_file(session: common_seccion,
                      serial: Annotated[str, Form()],
                      passwd: Annotated[str, Form()],
                      user_data: Annotated[dict, router.dependencies[0]]):

    personal = ConfiguracionService(session).get_personal(user_data['cedula'])
    if personal.permisos in [None, 'r', 'rw']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="requiere permisos para realizar esta accion"
        )

    data = ConfiguracionService(session).send_config_on_device(passwd, serial)
    if type(data) != bool:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return {'sms': 'configuracion enviada'}

@router.delete('/{id}',
               response_model=ConfiguracionSchema)
async def delete_config(session:common_seccion,
                        id: int | str,
                        user_data: Annotated[dict, router.dependencies[0]]):
    
    personal = ConfiguracionService(session).get_personal(user_data['cedula'])
    if personal.permisos != 'drwx':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="requiere permisos para realizar esta accion"
        )

    data = ConfiguracionService(session).delete_config(id)
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data
    

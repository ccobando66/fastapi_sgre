from ..services.admin import Admin as AdminService
from ..services.admin import AdminCreate, AdminSchema
from ..services.user import UserShema
from .base_module import *

router = APIRouter(
    prefix="/admin",
    tags=['Admin'],
    dependencies=[Depends(is_super_user)]
)


@router.get('/whoami', response_model=AdminSchema)
async def read_admin(session: common_seccion, cedula: Annotated[str, router.dependencies[0]]):

    data = AdminService(session).get_admin(cedula)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='no existe usuario en la base de datos'
        )
    return data


@router.post('/', response_model=AdminSchema)
async def set_admin(admin_model: AdminCreate, session: common_seccion):
    get_data = AdminService(session).create_admins(admin_model)
    if type(get_data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data


@router.delete('/{cedula}/admin', response_model=AdminSchema)
async def remove_admin(cedula: str, session: common_seccion):
    get_data = AdminService(session).delete_admin(cedula)
    if type(get_data) == str:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=get_data
        )
    return get_data


# funtion admin
@router.put('/{cedula}/admin/unlock', response_model=UserShema)
async def unlock_user(cedula: str, session: common_seccion):
    get_data = AdminService(session).desbloquear_user(cedula)
    if type(get_data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data


@router.put('/{cedula}/admin/lock', response_model=UserShema)
async def lock_user(cedula: str, session: common_seccion):
    get_data = AdminService(session).bloquear_user(cedula)
    if type(get_data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data


@router.put('/{cedula}/admin/roll', response_model=UserShema | None)
async def add_roll_user(cedula: str, session: common_seccion):
    get_data = AdminService(session).asignar_rol_super_usuario(cedula)
    if type(get_data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data

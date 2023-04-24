from .base_module import *

from ..services.user import (
    UserShema,UserCreate,
    User as UserService
)



router = APIRouter(
    prefix='/user',
    tags=['User']
    
)

@router.get(
    path='/{cedula}',
    response_model=UserShema
)
async def read_user(cedula: str, seccion: common_seccion):
    data = UserService(seccion).get_user(cedula)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='no existe usuario en la base de datos'
        )
    return data

@router.get(
    path='/',
    response_model=List[UserShema]
)
async def read_many_users(skip: int, limit:int, seccion: common_seccion):
    return UserService(seccion).get_users(skip,limit)

@router.post(
    path='/',
    response_model=UserShema
)
async def set_user(user_schema:UserCreate,seccion: common_seccion):
    get_data = UserService(seccion).create_user(user_schema)
    if type(get_data) == str:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data 

@router.patch(
    path='/',
    response_model=UserShema
)
async def modify_user(user_schema:UserCreate,seccion: common_seccion):
    get_data = UserService(seccion).update_user(user_schema)
    if type(get_data) == str:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data

@router.delete(
    path='/{cedula}/delete',
    response_model=UserShema
)
async def remove_user(cedula: str,seccion: common_seccion):
    get_data = UserService(seccion).delete_user(cedula)
    if type(get_data) == str:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=get_data
        )
    return get_data 
    
    
    
    

        
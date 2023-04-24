from .base_module import *

from ..services.personal import (
    PersonalShema,PersonalCreate,
    Personal as PersonalService
)


router = APIRouter(
    prefix='/personal',
    tags=['Personal']
    
)

@router.get(
    path='/{cedula}',
    response_model=PersonalShema
)
async def read_personal(cedula: str, seccion: common_seccion):
    data = PersonalService(seccion).get_personal(cedula)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='no existe usuario en la base de datos'
        )
    return data

@router.get(
    path='/',
    response_model=List[PersonalShema]
)
async def read_many_personal(skip: int, limit:int, seccion: common_seccion):
    return PersonalService(seccion).get_personas(skip,limit)

@router.post(
    path='/'
)
async def set_personal(personal_schema:PersonalCreate,seccion: common_seccion):
    get_data = PersonalService(seccion).create_personal(personal_schema)
    if type(get_data) == str:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data 

"""
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
"""

@router.delete(
    path='/{cedula}/delete',
    response_model=PersonalShema
)
async def remove_user(cedula: str,seccion: common_seccion):
    get_data = PersonalService(seccion).delete_personal(cedula)
    if type(get_data) == str:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=get_data
        )
    return get_data 

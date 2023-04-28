from .base_module import *

from ..services.user import (
    UserShema,UserCreate,
    User as UserService
)


router = APIRouter(
    prefix='/user',
    tags=['User'],
    dependencies=[Depends(get_valid_user)]
    
)

@router.get(
    path='/whoami',
    response_model=UserShema,
)
async def read_user(seccion: common_seccion,
                    datas: Annotated[dict,router.dependencies[0]]
                    ):
    
    data = UserService(seccion).get_user(datas['cedula'])
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='no existe usuario en la base de datos'
        )
    return data

@router.get(
    path='/',
    response_model=List[UserShema],
    dependencies=[Depends(is_super_user)]
)
async def read_many_users(skip: int, 
                          limit:int, 
                          seccion: common_seccion,
                          ):
    
    return UserService(seccion).get_users(skip,limit)



@router.patch(
    path='/',
    response_model=UserShema   
)
async def modify_user(user_schema:UserCreate,
                      seccion: common_seccion
                      ):
    get_data = UserService(seccion).update_user(user_schema)
    if type(get_data) == str:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data

@router.delete(
    path='/{cedula}/delete',
    response_model=UserShema,
    dependencies=[Depends(is_super_user)]
)
async def remove_user(cedula: str,
                      seccion: common_seccion,
                     ):
    
    
    get_data = UserService(seccion).delete_user(cedula)
    if type(get_data) == str:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=get_data
        )
    return get_data 

  
    
    

        
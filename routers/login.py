from .base_module import *

from ..services.user import (
    User as UserService, TokenSchema, 
    UserShema, UserCreate
)

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/login',
    tags=['Login']
    
)

@router.post(
    path='/',
    response_model=TokenSchema | None
)
async def login_user(user_schema:Annotated[OAuth2PasswordRequestForm,Depends()],
                     seccion: common_seccion):
    get_data = UserService(seccion).login_user(user_schema.username,user_schema.password)
    if type(get_data) == str:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data    

@router.post(
    path='/create',
    response_model=UserShema
)
async def set_user(user_schema:UserCreate,
                   seccion:common_seccion
                   ):
    get_data = UserService(seccion).create_user(user_schema)
    if type(get_data) == str:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data 
    
    

        
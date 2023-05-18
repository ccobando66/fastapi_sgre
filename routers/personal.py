from ..services.personal import Personal as PersonalService
from ..services.personal import PersonalCreate, PersonalShema
from .base_module import *

router = APIRouter(
    prefix='/personal',
    tags=['Personal'],
    dependencies=[Depends(get_valid_user)]

)

common_personal = Annotated[dict, router.dependencies[0]]


@router.get(
    path='/whoami',
    response_model=PersonalShema,
    response_model_exclude={'id'}

)
async def read_personal(seccion: common_seccion,
                        datas: common_personal):
    print(datas)
    data = PersonalService(seccion).get_personal(datas['cedula'])
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='no existe usuario en la base de datos'
        )
    return data


@router.get(
    path='/',
    response_model=Dict[str,List[PersonalShema] | Any] ,
    dependencies=[Depends(is_super_user)]
)
async def read_many_personal(page: Annotated[int, Query(..., gt=0)],
                             max_page: Annotated[int, Query(..., ge=10)],
                             seccion: common_seccion
                             ):

    data = PersonalService(seccion).get_personas(page, max_page)
    return {
        'data': data[0],
        'page': page,
        'start': data[1],
        'end': data[2],
        'total': max_page
    }


@router.post(
    path='/',
    dependencies=[Depends(is_super_user)],
    response_model=PersonalShema,
    status_code=status.HTTP_201_CREATED
)
async def set_personal(personal_schema: PersonalCreate,
                       seccion: common_seccion):
    get_data = PersonalService(seccion).create_personal(personal_schema)
    if type(get_data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data


@router.patch(
    path='/',
    dependencies=[Depends(is_super_user)],
    response_model=PersonalShema
)
async def modify_user(user_schema: PersonalCreate, seccion: common_seccion):
    get_data = PersonalService(seccion).update_personal(user_schema)
    if type(get_data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_data
        )
    return get_data


@router.delete(
    path='/{cedula}/delete',
    dependencies=[Depends(is_super_user)],
    response_model=PersonalShema
)
async def remove_user(cedula: str, seccion: common_seccion):
    get_data = PersonalService(seccion).delete_personal(cedula)
    if type(get_data) == str:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=get_data
        )
    return get_data

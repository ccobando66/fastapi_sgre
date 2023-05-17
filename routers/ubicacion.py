from ..services.ubicacion import RackCreate, RackSchema
from ..services.ubicacion import Ubicacion as UbicacionService
from ..services.ubicacion import UbicacionCreate, UbicacionSchema
from .base_module import *


router = APIRouter(prefix='/ubicacion',
                   tags=['Ubicacion'])


@router.post('/',
             response_model=UbicacionSchema,
             status_code=status.HTTP_201_CREATED)
async def set_ubicacion(ubcacion_schema: UbicacionCreate,
                        session: common_seccion):

    data = UbicacionService(session).create_ubicacion(ubcacion_schema,'1012432367')
    if type(data) == str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data
        )
    return data

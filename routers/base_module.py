from fastapi import (
    APIRouter, HTTPException,status,
    Depends
)

from typing import Annotated, List
from sqlalchemy.orm import Session

from ..dependencies import get_session
common_seccion = Annotated[Session,Depends(get_session)]
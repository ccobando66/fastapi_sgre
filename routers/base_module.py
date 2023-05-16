from typing import Annotated, Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..dependencies import get_session, get_valid_user, is_super_user,is_personal_user

common_seccion = Annotated[Session,Depends(get_session)]

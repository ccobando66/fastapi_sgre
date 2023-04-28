from .config.database import SessionLocal
from .auth.oauth2 import decode_token


from typing import Annotated, Any
from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        

async def get_valid_user(user:Annotated[dict,Depends(decode_token)]):
    to_decode = user.copy()
    if to_decode['is_actived'] == False:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Usuario inactivo"
           
       ) 
    return to_decode

def is_super_user(user:Annotated[dict,Depends(get_valid_user)]):
    to_decode = user.copy()
    if to_decode['is_super_user'] == False:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="requere permisos de superusuario para esta accion"
           
       ) 



    
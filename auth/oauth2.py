from datetime import datetime
from os import getenv
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..config.database import SessionLocal, get_session
from ..models.user import User

scheme_login = OAuth2PasswordBearer(tokenUrl='/login/')


def create_token(data: dict) -> str | None:
    try:
        encode_jwt = jwt.encode(data, getenv(
            'JWT_SECRET'), algorithm=getenv('JWT_ALGORITH'))
        return encode_jwt
    except JWTError as ex:
        print(ex)
        return None


def decode_token(token: Annotated[str, Depends(scheme_login)],
                 session: Annotated[Session, Depends(get_session)]
                 ):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="credenciales no validos",
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:

        payload = jwt.decode(token, getenv('JWT_SECRET'),
                             algorithms=[getenv('JWT_ALGORITH')])

        data = session.query(User.is_actived,
                             User.is_super_user,
                             User.cedula
                             ).filter(User.cedula == payload['user_cedula']
                                      ).first()

        if data is None or datetime.isoformat(datetime.now()) >= payload['caducidad']:
            raise credential_exception

        return data._asdict()
    except JWTError:
        raise credential_exception

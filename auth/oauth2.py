from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

scheme_login = OAuth2PasswordBearer(tokenUrl='/user/login')


def create_token(data:dict) -> str:
    to_encode = data.copy()
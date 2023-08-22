from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt


class JWTUtil:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
    ALGORITHM = "HS256"
    # JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    JWT_SECRET_KEY = "cdbgsbcnbcghdsvdscmnndjvdsgvcbdjsbvdsbcdsc"  # should be kept secret
    # JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']  # should be kept secret
    JWT_REFRESH_SECRET_KEY = "gfascdgbschdbnnshsddcjdbvhgsxsaduyhdbchgdvch"
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return JWTUtil.password_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_pass: str) -> bool:
        return JWTUtil.password_context.verify(password, hashed_pass)

    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=JWTUtil.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWTUtil.JWT_SECRET_KEY, JWTUtil.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=JWTUtil.REFRESH_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWTUtil.JWT_REFRESH_SECRET_KEY, JWTUtil.ALGORITHM)
        return encoded_jwt

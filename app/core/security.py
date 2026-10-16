form datetime import datetime
from datetime import timedelta

from jose import JWTError
from jose import jwt

from passlib.context import CryptContext

from app.core.config import settings

ALGORITHM = 'HS256'

pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(
        plain_password: str,
        password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def create_access_token(
        user_id: int,
        login: str,
        role: str,
) -> str:
    payload = {
        "sub": str(user_id),
        "login": login,
        "role": role,
        "exp": datetime.datetime.now() + timedelta(hours=8)
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

def encode_token(
        token: str,
) -> dict|None:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        return None

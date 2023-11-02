from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from config import CONFIG

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, CONFIG.secret_key, algorithm="HS256")
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

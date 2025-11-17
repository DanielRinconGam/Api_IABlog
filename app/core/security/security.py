from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings
from passlib.exc import UnknownHashError

# Configuración recomendada por OWASP para Argon2id
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,      # 64 MB
    argon2__parallelism=2,
    argon2__time_cost=3,
    argon2__hash_len=32,
    argon2__type="ID"               # Argon2id (más seguro)
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except UnknownHashError:
        # Manejar casos donde el hash no es Argon2
        return False

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, settings.JWT_ALGORITHM)

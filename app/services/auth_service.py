from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security.security import hash_password, verify_password, create_token
from sqlalchemy.exc import SQLAlchemyError

def register_user(db: Session, email: str, password: str, nickname: str):
    """
    Registra un usuario asegurando que el email sea único
    y aplicando hashing Argon2.
    """
    exists = db.query(User).filter(User.email == email).first()
    if exists:
        raise ValueError("Este email ya está registrado.")

    try:
        user = User(
            email=email,
            password_hash=hash_password(password),
            nickname=nickname
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error al registrar el usuario: {str(e)}")


def authenticate_user(db: Session, email: str, password: str):
    """
    Valida credenciales verificando la contraseña con Argon2.
    Devuelve el usuario si es válido; de lo contrario, None.
    """
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def generate_token_for_user(user: User):
    """
    Genera token JWT con el ID del usuario.
    """
    return create_token({"sub": str(user.id)})

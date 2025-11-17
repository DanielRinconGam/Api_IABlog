from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, Token
from app.services.auth_service import register_user, authenticate_user, generate_token_for_user

from app.core.security.dependencies import get_current_user
from app.models.user import User

router = APIRouter(tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario con Argon2 y retorna id y email.
    """
    try:
        user = register_user(db, payload.email, payload.password)
        return {"id": user.id, "email": user.email}

    except ValueError as e:
        # Por ejemplo: email already registered
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/token", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica al usuario y devuelve un JWT si las credenciales son correctas.
    """
    user = authenticate_user(db, payload.email, payload.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = generate_token_for_user(user)

    return Token(access_token=token)

@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

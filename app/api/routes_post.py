from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.post_service import create_post, list_posts, get_post
from app.schemas.post import PostCreate, PostOut, PromptRequest
from app.services.ia_service import generate_blog_post
from app.core.security.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/generate", response_model=PostOut)
def create_ai_post(payload: PromptRequest,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    
    base_url = "http://localhost:8000"  # O settings.BASE_URL

    post_schema = generate_blog_post(payload.prompt, base_url)
    return create_post(db, post_schema, current_user.id)


@router.get("/", response_model=list[PostOut])
def all_posts(db: Session = Depends(get_db)):
    return list_posts(db)


@router.get("/{post_id}", response_model=PostOut)
def one_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(404, "Post no encontrado")
    return post

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.deps import get_current_user
from app.schemas.post import PromptRequest, PostOut
from app.services.ia_service import generate_blog_post
from app.services.post_service import create_post

router = APIRouter()

@router.post("/generate-post", response_model=PostOut)
def generate_post(
    payload: PromptRequest,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    base_url = str(request.base_url).rstrip("/")

    post_data = generate_blog_post(payload.prompt, base_url)
    saved = create_post(db, post_data, user.id)
    return saved

from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.image import Image
from app.schemas.post import PostCreate


def create_post(db: Session, post_data: PostCreate, author_id: int) -> Post:
    """Crear un post incluyendo sus imágenes."""
    # Crear el post base
    post = Post(
        title=post_data.title,
        body=post_data.body,
        seo_description=post_data.seo_description,
        author_id=author_id
    )

    db.add(post)
    db.flush()  # Esto obtiene post.id sin hacer commit aún

    # Crear las imágenes asociadas
    for img in post_data.images:
        db.add(
            Image(
                url=str(img.url),
                description=img.description,
                post_id=post.id
            )
        )

    db.commit()
    db.refresh(post)
    return post


def list_posts(db: Session):
    """Listar todos los posts ordenados por fecha (más recientes primero)."""
    return db.query(Post).order_by(Post.created_at.desc()).all()


def get_post(db: Session, post_id: int) -> Post | None:
    """Obtener un post por ID con sus imágenes."""
    return db.query(Post).filter(Post.id == post_id).first()


def delete_post(db: Session, post_id: int) -> bool:
    """Eliminar un post y sus imágenes asociadas gracias a ON DELETE CASCADE."""
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return False

    db.delete(post)
    db.commit()
    return True

def list_posts_by_user(db: Session, user_id: int):
    """Obtener todos los posts de un usuario específico ordenados por fecha (más recientes primero)"""
    return db.query(Post).filter(Post.author_id == user_id).order_by(Post.created_at.desc()).all()


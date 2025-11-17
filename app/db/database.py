from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from sqlalchemy.engine.url import URL

# Validación para evitar errores cuando falte la variable
if not settings.DATABASE_URL:
    raise Exception("DATABASE_URL no está configurada en las variables de entorno.")

# Render Postgres requiere SSL en algunos planes
# Le añadimos sslmode=require si no existe
db_url = settings.DATABASE_URL

if "sslmode" not in db_url and db_url.startswith("postgresql"):
    db_url += "?sslmode=require"

engine = create_engine(
    db_url,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_auth, routes_post, routes_ai
from app.core.config import settings
from app.db.database import Base, engine
from app.models import *

app = FastAPI(title="IA Blog API", version="1.0.0")
origins = [settings.GITHUB_PAGES_ORIGIN]


@app.get("/")
def root():
    return {"msg": "Esta es la API para dar vida al blog!"}

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_auth.router)
app.include_router(routes_post.router)
app.include_router(routes_ai.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

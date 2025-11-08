from fastapi import FastAPI

app = FastAPI(title="IA Blog API", version="1.0.0")

@app.get("/")
def root():
    return {"msg": "Esta es la API para dar vida al blog!"}
from fastapi import FastAPI
from config.database import engine, Base
from routes import auth

# Crear tablas si faltara alguna
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi API Mobile - FastAPI")

# Registrar las rutas de autenticación
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente al 100%"}
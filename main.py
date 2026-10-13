from fastapi import FastAPI
from config.database import engine, Base
from routes import auth
from fastapi.middleware.cors import CORSMiddleware

# Crear tablas si faltara alguna
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi API Mobile - FastAPI")

# Agregar middleware inmediatamente después de crear la app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"], # Solo tu web local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas de autenticación
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente al 100%"}
#guardate
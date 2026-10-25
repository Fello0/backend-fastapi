from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import Base, engine

# 1. DEBES IMPORTAR TODOS LOS ARCHIVOS DE RUTAS AQUÍ:
from routes import auth, product, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Full Stack Móvil")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. DEBES REGISTRAR TODAS LAS RUTAS AQUÍ:
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API conectada correctamente"}

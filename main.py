from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import Base, engine

# 1. DEBES IMPORTAR AMBOS ARCHIVOS DE RUTAS AQUÍ:
from routes import auth, product

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Full Stack Móvil")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. DEBES REGISTRAR AMBAS RUTAS AQUÍ:
app.include_router(auth.router)
app.include_router(product.router)  # <-- ESTA ES LA LÍNEA QUE TE FALTA

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API conectada correctamente"}
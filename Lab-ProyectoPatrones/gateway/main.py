from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modulos.registro.logica.registro_service import router as registro_router

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(registro_router, prefix="/registro")

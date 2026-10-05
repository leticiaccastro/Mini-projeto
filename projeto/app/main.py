from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.tarefas import router as tarefas_router


app = FastAPI(
    title="API de Tarefas - SENAI",
    version="1.0.0",
    description="Sistema de gerenciamento de tarefas. Modulo 2"
)


# Permite que o Front-end acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas de tarefas
app.include_router(tarefas_router)


# ==========================================================
# ROTA PRINCIPAL
# ==========================================================

@app.get("/", tags=["Geral"])
def status_api():

    return {
        "mensagem": "API de Tarefas funcionando!",
        "status": "online"
    }
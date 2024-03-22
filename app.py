from fastapi import FastAPI
from users.routes import router as user_router
from turmas.routes import router as turmas_router
from propostas.routes import router as propostas_router

app = FastAPI()

# Montando as rotas de usuário diretamente
app.include_router(user_router)
app.include_router(turmas_router)
app.include_router(propostas_router)

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from users.routes import router as user_router
from turmas.routes import router as turmas_router
from propostas.routes import router as propostas_router
from generos.routes import router as generos_router
from redacoes.routes import router as redacoes_router
from correcoes.routes import router as correcoes_router
from auth.routes import router as auth_router


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Origem do frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Montando as rotas de usuário diretamente
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(turmas_router)
app.include_router(propostas_router)
app.include_router(generos_router)
app.include_router(redacoes_router)
app.include_router(correcoes_router)
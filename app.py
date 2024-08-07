from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from users.routes import router as user_router
from turmas.routes import router as turmas_router
from propostas.routes import router as propostas_router
from generos.routes import router as generos_router
from redacoes.routes import router as redacoes_router
from correcoes.routes import router as correcoes_router
from auth.routes import router as auth_router
from turmas_has_users.routes import router as turmas_has_users_router
from users_has_cidades.routes import router as users_has_cidades_router
from propostas_has_turmas.routes import router as propostas_has_turmas_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    
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
app.include_router(turmas_has_users_router)
app.include_router(users_has_cidades_router)
app.include_router(propostas_has_turmas_router)
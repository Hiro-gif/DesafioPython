from fastapi import FastAPI
from app.routers import app_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Web Scraping API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

app.include_router(app_router)


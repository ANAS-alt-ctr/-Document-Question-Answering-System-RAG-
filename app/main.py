from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Document Q/A RAG API"
)

app.include_router(router)
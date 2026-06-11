from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.routes import auth, note

from app.db.base import Base
from app.db.base import engine

from app.models.user import User
from app.models.note import Note

Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="Team Productivity Platform API",
    description="""
    FastAPI Service
    
    Responsibilities:
    - Authentication
    - User Management
    - Notes Management
    - Open Library Integration
    - Notes → Task Conversation
    
    Consumed by Next.js Frontend.
    Shared JWT Authentication with NestJS.
    """,
    version="1.0.0",
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origin=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service":"FastAPI",
        "name":"Team Productivity Platform",
        "status": "running",
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

app.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["Authentication"]
)

app.include_router(
    note.router,
    prefix="/api/v1",
    tags=["Notes"]
)

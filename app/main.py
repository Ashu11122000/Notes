from fastapi import FastAPI # type: ignore

from app.core.config import settings

from app.api.routes import auth, note

from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy registers them
from app.models.user import User  # noqa: F401
from app.models.note import Note  # noqa: F401


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)


# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Notes Backend is running"
    }


# Routes
app.include_router(auth.router)
app.include_router(note.router)
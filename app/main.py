from fastapi import FastAPI
from app.core.config import settings

from app.api.routes import auth, note

# Import Base and engine
from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy can detect them
from app.models.user import User
from app.models.note import Note


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)


# Create tables on startup
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Notes Backend is running"}


app.include_router(auth.router)
app.include_router(note.router)
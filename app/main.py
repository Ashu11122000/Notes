from fastapi import FastAPI
from app.core.config import settings

from app.api.routes import auth, note

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)


@app.get("/")
def root():
    return {"message": "Notes Backend is running"}

app.include_router(auth.router)
app.include_router(note.router)
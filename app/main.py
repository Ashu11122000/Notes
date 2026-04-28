from fastapi import FastAPI
from app.core.config import settings

# Import routers
from app.api.routes import auth

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)


# Root endpoint
@app.get("/")
def root():
    return {"message": "Notes Backend is running 🚀"}


# Include Auth routes
app.include_router(auth.router)
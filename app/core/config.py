from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str
    DEBUG: bool

    # Server
    HOST: str
    PORT: int

    # Database
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    class Config:
        env_file = ".env"


settings = Settings()
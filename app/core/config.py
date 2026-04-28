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
    DB_PORT: str
    DB_PASSWORD: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()
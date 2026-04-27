from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str
    debug: bool

    # Server
    host: str
    port: int

    # Database
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # JWT
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
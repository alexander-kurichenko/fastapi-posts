from pydantic import BaseSettings


class Settings(BaseSettings):
    db_type: str
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str
    access_token_algorithm: str
    access_token_secret_key: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"


settings = Settings()

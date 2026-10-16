from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AutoBreaking"

    SECRET_KEY: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = {
        "env_file": ".env"
    }

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()
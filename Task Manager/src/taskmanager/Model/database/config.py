'postgresql+psycopg2://postgres:1234@localhost:5432/PostgreSQL'
from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_NAME}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="C:\\Users\\admin\\Desktop\\Учёба\\Task Manager\\.env")

setting = Setting()
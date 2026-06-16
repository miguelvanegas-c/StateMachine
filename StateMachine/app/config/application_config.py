# application_config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):


    API_HOST: str = Field(default="0.0.0.0", description="Host donde corre la API")
    API_PORT: int = Field(default=8000, description="Puerto de la API")
    DEBUG: bool = Field(default=True, description="Modo debug")
    PROJECT_NAME: str = Field(default="TeamsAndTask", description="Nombre del proyecto")


    # MongoDB configuration. If MONGODB_URL is provided in the environment, it will be used.
    MONGO_USER: str = Field(default="mongo", description="Usuario de MongoDB")
    MONGO_PASSWORD: str = Field(default="mongo", description="Password de MongoDB")
    MONGO_HOST: str = Field(default="localhost", description="Host de MongoDB")
    MONGO_PORT: int = Field(default=27017, description="Puerto de MongoDB")
    MONGO_DB: str = Field(default="teamsandtask_db", description="Nombre de la base de datos MongoDB")

    MONGODB_URL: Optional[str] = Field(
        default=None,
        description="URL completa de MongoDB. Si está presente se usa en lugar de MONGO_* individuales"
    )



    ENVIRONMENT: str = Field(
        default="development",
        description="Entorno: development, staging, production"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"



settings = Settings()

# Helper property: construir la URI si no se pasa MONGODB_URL
def _build_mongo_uri(s: Settings) -> str:
    if s.MONGODB_URL:
        return s.MONGODB_URL
    return f"mongodb://{s.MONGO_USER}:{s.MONGO_PASSWORD}@{s.MONGO_HOST}:{s.MONGO_PORT}/{s.MONGO_DB}?authSource=admin"

# Exponer una propiedad legible desde otros módulos
Settings.MONGO_URI = property(_build_mongo_uri)

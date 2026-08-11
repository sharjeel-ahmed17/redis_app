from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env" , extra="ignore")

    DB_URI : str
    REDIS_URI : str = "redis://localhost:6379/0"

    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    MAIL_USERNAME : str
    MAIL_PASSWORD : str

settings= Settings()

# print(settings.DB_URI)
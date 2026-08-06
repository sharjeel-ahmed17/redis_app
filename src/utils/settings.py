from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env" , extra="ignore")

    DB_URI : str


settings= Settings()

# print(settings.DB_URI)
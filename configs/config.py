from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    OAUTH2_URL: str = ""
    OAUTH2_TOKEN: str = ""
    DB_CONFIG: str
    AZURE_TENANT_ID: str 
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    VS_AZURE_SCOPE: str
    WF_BASE_URL: str = ""
    WF_CLIENT_ID: str = ""
    WF_PUBLIC_KEY: str = ""

settings = Settings()
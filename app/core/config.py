from pydantic import BaseModel


class Settings(BaseModel):
    DATABASE_URL: str = "sqlite+aiosqlite:///./crm.db"
    APP_TITLE: str = "Mini CRM Leads Distribution"


settings = Settings()

from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="bagusanmana?")
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="INFO")
    
    # CORS
    CORS_ORIGINS: list[str] = Field(...)
    CORS_CREDENTIALS: bool = Field(default=True)
    CORS_METHODS: list[str] = Field(default=["*"])
    CORS_HEADERS: list[str] = Field(default=["*"])
    
    # KECERDASAN
    GEMINI_PROJECT_ID: Optional[str] = Field(default="")
    GEMINI_PROJECT_NAME: Optional[str] = Field(default="")
    GEMINI_API_KEY: str = Field(...)
    MODEL_ID: str = Field(default="gemini-2.0-flash-lite-preview")
    
    TOP_P: Optional[float] = Field(default=0.95)  
    OUTPUT_LENGTH: Optional[int] = Field(default=8192)
    TEMPERATURE: Optional[float] = Field(default=1.0) 
    HARRASMENT_SETTING: str = Field(default="BLOCK_LOW_AND_ABOVE")
    HATE_SPEECH_SETTING: str = Field(default="BLOCK_LOW_AND_ABOVE")
    SEXUALLY_EXPLICIT_SETTING: str = Field(default="BLOCK_LOW_AND_ABOVE")
    DANGEROUS_CONTENT_SETTING: str = Field(default="BLOCK_LOW_AND_ABOVE")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
@lru_cache
def get_settings() -> Settings:
    return Settings()
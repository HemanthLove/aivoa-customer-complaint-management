from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    groq_api_key: str
    groq_model: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()
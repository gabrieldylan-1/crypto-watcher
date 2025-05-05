from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Postgres
    POSTGRES_USER: str = "myuser"
    POSTGRES_PASSWORD: str = "mypassword"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_DB: str = "candles_db"
    PG_DSN: str = "postgresql://myuser:mypassword@postgres:5432/candles_db"

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB:   int = 0
    HISTORY_TTL_DAYS: int = 60

    # Scheduler
    RUN_EVERY_MIN: int = 5

    # Alert channels
    TEAMS_WEBHOOK: str = ""
    TELE_TOKEN: str = ""
    TELE_CHATID: int = 0

    # Rule engine
    THRESHOLD_FILE: str = "./config/thresholds.yaml"
    MODE: str = "rule"      # rule | prophet | pyod
    CONSECUTIVE: int = 2
    COOLDOWN_MIN: int = 30
    
    PYTHONPATH: str = "/"

    class Config:
        env_file = "../.env"

settings = Settings()
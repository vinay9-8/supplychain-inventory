from collections.abc import Mapping
import os
from pathlib import Path

from sqlalchemy.engine import URL, make_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _build_database_url(environment: Mapping[str, str] | None = None) -> URL | None:
    env = os.environ if environment is None else environment
    database_url = env.get("DATABASE_URL")
    if database_url:
        url = make_url(database_url)
        if url.drivername == "mysql":
            url = url.set(drivername="mysql+pymysql")
        return url

    required = ("DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD")
    configured = any(env.get(name) for name in required)
    if not configured:
        return None

    missing = [name for name in required if not env.get(name)]
    if missing:
        raise ValueError(
            "Incomplete MySQL configuration; set " + ", ".join(missing)
        )

    return URL.create(
        "mysql+pymysql",
        username=env["DB_USER"],
        password=env["DB_PASSWORD"],
        host=env["DB_HOST"],
        port=int(env.get("DB_PORT", "3306")),
        database=env["DB_NAME"],
        query={"charset": "utf8mb4"},
    )


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    APP_ENV = os.getenv("APP_ENV", "development")
    SQLALCHEMY_DATABASE_URI = _build_database_url()
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() in {"1", "true", "yes", "on"}
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "*")


class TestingConfig(Config):
    APP_ENV = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS = {}

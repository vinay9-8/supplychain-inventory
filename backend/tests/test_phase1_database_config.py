import pytest
from sqlalchemy.engine import make_url

from backend.app import create_app
from backend.config import TestingConfig, _build_database_url


def test_mysql_url_uses_environment_credentials_and_utf8mb4():
    url = _build_database_url({
        "DB_HOST": "db.example",
        "DB_PORT": "3307",
        "DB_NAME": "supply_chain",
        "DB_USER": "inventory app",
        "DB_PASSWORD": "p@ss/word",
    })

    assert url is not None
    assert url.drivername == "mysql+pymysql"
    assert url.host == "db.example"
    assert url.port == 3307
    assert url.database == "supply_chain"
    assert url.username == "inventory app"
    assert url.password == "p@ss/word"
    assert url.query["charset"] == "utf8mb4"


def test_database_url_override_takes_precedence_and_uses_pymysql():
    url = _build_database_url({
        "DATABASE_URL": "mysql://user:password@db.example:3308/supply_chain",
        "DB_HOST": "ignored",
        "DB_NAME": "ignored",
        "DB_USER": "ignored",
        "DB_PASSWORD": "ignored",
    })

    assert url is not None
    assert url.drivername == "mysql+pymysql"
    assert url.host == "db.example"
    assert url.port == 3308


def test_partial_mysql_environment_is_rejected():
    with pytest.raises(ValueError, match="Incomplete MySQL configuration"):
        _build_database_url({"DB_HOST": "db.example"})


def test_missing_database_configuration_does_not_fall_back_to_sqlite():
    class UnconfiguredConfig(TestingConfig):
        APP_ENV = "development"
        SQLALCHEMY_DATABASE_URI = None

    with pytest.raises(RuntimeError, match="Database is not configured"):
        create_app(UnconfiguredConfig)


def test_test_configuration_is_the_only_supported_sqlite_configuration():
    class SqliteDevelopmentConfig(TestingConfig):
        APP_ENV = "development"

    with pytest.raises(RuntimeError, match="SQLite is supported only with TestingConfig"):
        create_app(SqliteDevelopmentConfig)


def test_test_configuration_uses_sqlite():
    app = create_app(TestingConfig)

    assert make_url(app.config["SQLALCHEMY_DATABASE_URI"]).get_backend_name() == "sqlite"

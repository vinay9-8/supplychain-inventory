import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import make_url

try:
    from .config import Config
    from .extensions import db, migrate
except ImportError:  # pragma: no cover - support running as a script
    from config import Config
    from extensions import db, migrate

from backend import models as model_registry
from backend.generators.data_generator import DataGenerator
from backend.routes.dashboard import dashboard_bp
from backend.routes.forecasts import forecasts_bp
from backend.routes.inventory import inventory_bp
from backend.routes.mitigation import mitigation_bp
from backend.routes.purchase_orders import purchase_orders_bp
from backend.routes.shortages import shortages_bp
from backend.routes.suppliers import suppliers_bp


REQUIRED_DATA_FILES = [
    "skus.csv",
    "locations.csv",
    "suppliers.csv",
    "inventory.csv",
    "forecast_demand.csv",
    "purchase_orders.csv",
    "supplier_capacity.csv",
    "lead_times.csv",
]
REQUIRED_MODEL_NAMES = {
    "Sku",
    "Location",
    "ForecastDemand",
    "Inventory",
    "Supplier",
    "SupplierCapacity",
    "LeadTime",
    "PurchaseOrder",
    "ProductionPlan",
    "Shortage",
    "MitigationOption",
}


def ensure_generated_data(root_dir: str | Path | None = None, mode: str = "sample") -> None:
    target_root = Path(root_dir) if root_dir is not None else Path(__file__).resolve().parents[1]
    generated_dir = target_root / "data" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    missing = [name for name in REQUIRED_DATA_FILES if not (generated_dir / name).exists()]
    if missing:
        generator = DataGenerator(seed=20261022, root_dir=target_root)
        generator.generate_dataset(mode=mode, persist=True)
        print(f"Generated missing dataset files for {target_root}: {', '.join(missing)}")


def _configure_logging(app: Flask) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        ))
        logger.addHandler(handler)

    app.logger.handlers = logger.handlers
    app.logger.setLevel(logging.INFO)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    missing_models = REQUIRED_MODEL_NAMES.difference(model_registry.__all__)
    if missing_models:
        raise RuntimeError(f"SQLAlchemy models are not registered: {', '.join(sorted(missing_models))}")

    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    if not database_uri:
        raise RuntimeError(
            "Database is not configured. Set DATABASE_URL or "
            "DB_HOST, DB_NAME, DB_USER, and DB_PASSWORD."
        )
    if app.config.get("APP_ENV") != "testing" and make_url(database_uri).get_backend_name() != "mysql":
        raise RuntimeError("SQLite is supported only with TestingConfig; configure MySQL for the application.")

    app.config.setdefault("APP_START_TIME", time.time())
    _configure_logging(app)

    allowed_origins = app.config.get("CORS_ALLOWED_ORIGINS", "*")
    if allowed_origins and allowed_origins != "*":
        origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]
    else:
        origins = "*"

    CORS(app, resources={
        r"/api/*": {"origins": origins},
        r"/health": {"origins": origins},
        r"/health/database": {"origins": origins},
    })
    db.init_app(app)
    migrate.init_app(
        app,
        db,
        directory=str(Path(__file__).resolve().parent / "migrations"),
        compare_type=True,
    )

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        if app.config.get("APP_ENV") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response

    app.register_blueprint(dashboard_bp, url_prefix="/api")
    app.register_blueprint(inventory_bp, url_prefix="/api")
    app.register_blueprint(suppliers_bp, url_prefix="/api")
    app.register_blueprint(forecasts_bp, url_prefix="/api")
    app.register_blueprint(purchase_orders_bp, url_prefix="/api")
    app.register_blueprint(shortages_bp, url_prefix="/api")
    app.register_blueprint(mitigation_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return jsonify({
            "status": "ok",
            "service": "supply-chain-inventory-optimization",
            "environment": app.config.get("APP_ENV", "development"),
        })

    @app.get("/health/database")
    def database_health():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except SQLAlchemyError:
            app.logger.exception("Database health check failed")
            return jsonify({
                "status": "error",
                "database": {
                    "status": "unavailable",
                },
            }), 503

        return jsonify({
            "status": "ok",
            "database": {
                "status": "connected",
                "dialect": db.engine.dialect.name,
            },
        })

    @app.get("/api")
    def api_root():
        return jsonify({
            "message": "Supply chain API is running",
            "endpoints": [
                "/api/health",
                "/health/database",
                "/api/dashboard/summary",
                "/api/dashboard/export",
                "/api/inventory",
                "/api/suppliers",
                "/api/forecasts",
                "/api/purchase-orders",
                "/api/shortages",
                "/api/mitigation",
            ],
        })

    @app.get("/api/health")
    def api_health():
        return health()

    @app.get("/api/metrics")
    def metrics():
        uptime_seconds = max(0.0, time.time() - app.config["APP_START_TIME"])
        payload = {
            "status": "ok",
            "service": "supply-chain-inventory-optimization",
            "environment": app.config.get("APP_ENV", "development"),
            "uptime_seconds": round(uptime_seconds, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "python_version": __import__("platform").python_version(),
        }
        return jsonify(payload)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)

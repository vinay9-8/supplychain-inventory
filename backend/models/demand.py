from datetime import date

from backend.extensions import db
from backend.models.base import TimestampMixin


class ForecastDemand(db.Model, TimestampMixin):
    __tablename__ = "forecast_demand"
    __table_args__ = (
        db.UniqueConstraint(
            "sku_id",
            "location_id",
            "week_start",
            "model_version",
            name="uq_forecast_sku_location_week_version",
        ),
    )

    id = db.Column(db.String(64), primary_key=True)
    sku_id = db.Column(db.String(32), db.ForeignKey("skus.id"), nullable=False)
    location_id = db.Column(db.String(32), db.ForeignKey("locations.id"), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    forecast_units = db.Column(db.Float, nullable=False)
    lower_bound = db.Column(db.Float, default=0.0)
    upper_bound = db.Column(db.Float, default=0.0)
    forecast_method = db.Column(db.String(80), default="baseline")
    model_version = db.Column(db.String(40), default="v1")
    lifecycle_status = db.Column(db.String(32), default="active")

    sku = db.relationship("Sku", back_populates="demand")
    location = db.relationship("Location", back_populates="demand")

    def __repr__(self):
        return f"<ForecastDemand {self.id}>"

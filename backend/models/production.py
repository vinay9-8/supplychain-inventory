from datetime import date

from backend.extensions import db
from backend.models.base import TimestampMixin


class ProductionPlan(db.Model, TimestampMixin):
    __tablename__ = "production_plans"

    id = db.Column(db.String(64), primary_key=True)
    sku_id = db.Column(db.String(32), db.ForeignKey("skus.id"), nullable=False)
    location_id = db.Column(db.String(32), db.ForeignKey("locations.id"), nullable=False)
    planned_quantity = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(32), default="planned")
    lifecycle_status = db.Column(db.String(32), default="active")

    sku = db.relationship("Sku", back_populates="production_plans")
    location = db.relationship("Location", back_populates="production_plans")

    def __repr__(self):
        return f"<ProductionPlan {self.id}>"

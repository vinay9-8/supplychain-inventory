from backend.extensions import db
from backend.models.base import TimestampMixin


class Location(db.Model, TimestampMixin):
    __tablename__ = "locations"

    id = db.Column(db.String(32), primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    warehouse_type = db.Column(db.String(80), default="DC")
    capacity_units = db.Column(db.Integer, default=0)
    lifecycle_status = db.Column(db.String(32), default="active")

    inventory = db.relationship("Inventory", back_populates="location")
    demand = db.relationship("ForecastDemand", back_populates="location")
    purchase_orders = db.relationship("PurchaseOrder", back_populates="location")
    production_plans = db.relationship("ProductionPlan", back_populates="location")
    shortages = db.relationship("Shortage", back_populates="location")
    lead_times = db.relationship("LeadTime", back_populates="location")

    def __repr__(self):
        return f"<Location {self.code}>"

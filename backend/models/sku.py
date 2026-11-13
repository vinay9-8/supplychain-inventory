from backend.extensions import db
from backend.models.base import TimestampMixin


class Sku(db.Model, TimestampMixin):
    __tablename__ = "skus"

    id = db.Column(db.String(32), primary_key=True)
    sku_code = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(120), default="")
    unit_of_measure = db.Column(db.String(32), default="EA")
    lifecycle_status = db.Column(db.String(32), default="active")

    inventory = db.relationship("Inventory", back_populates="sku")
    demand = db.relationship("ForecastDemand", back_populates="sku")
    purchase_orders = db.relationship("PurchaseOrder", back_populates="sku")
    production_plans = db.relationship("ProductionPlan", back_populates="sku")
    shortages = db.relationship("Shortage", back_populates="sku")
    supplier_capacities = db.relationship("SupplierCapacity", back_populates="sku")
    lead_times = db.relationship("LeadTime", back_populates="sku")
    suppliers = db.relationship("Supplier", secondary="sku_supplier", back_populates="skus")

    def __repr__(self):
        return f"<Sku {self.sku_code}>"

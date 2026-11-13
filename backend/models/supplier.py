from backend.extensions import db
from backend.models.base import TimestampMixin


class Supplier(db.Model, TimestampMixin):
    __tablename__ = "suppliers"

    id = db.Column(db.String(32), primary_key=True)
    supplier_code = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    supplier_type = db.Column(db.String(80), default="external")
    country = db.Column(db.String(120), default="")
    rating = db.Column(db.Float, default=0.0)
    lifecycle_status = db.Column(db.String(32), default="active")

    purchase_orders = db.relationship("PurchaseOrder", back_populates="supplier")
    capacities = db.relationship("SupplierCapacity", back_populates="supplier")
    lead_times = db.relationship("LeadTime", back_populates="supplier")
    skus = db.relationship("Sku", secondary="sku_supplier", back_populates="suppliers")

    def __repr__(self):
        return f"<Supplier {self.supplier_code}>"

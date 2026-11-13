from datetime import date

from backend.extensions import db
from backend.models.base import TimestampMixin


class SupplierCapacity(db.Model, TimestampMixin):
    __tablename__ = "supplier_capacity"
    __table_args__ = (
        db.UniqueConstraint(
            "supplier_id",
            "sku_id",
            "effective_from",
            name="uq_supplier_capacity_effective_start",
        ),
    )

    id = db.Column(db.String(64), primary_key=True)
    supplier_id = db.Column(db.String(32), db.ForeignKey("suppliers.id"), nullable=False)
    sku_id = db.Column(db.String(32), db.ForeignKey("skus.id"), nullable=False)
    capacity_units = db.Column(db.Float, nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    effective_to = db.Column(db.Date, nullable=True)
    lifecycle_status = db.Column(db.String(32), default="active")

    supplier = db.relationship("Supplier", back_populates="capacities")
    sku = db.relationship("Sku", back_populates="supplier_capacities")

    def __repr__(self):
        return f"<SupplierCapacity {self.id}>"

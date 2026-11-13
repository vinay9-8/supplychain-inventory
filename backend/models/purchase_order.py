from datetime import date

from backend.extensions import db
from backend.models.base import TimestampMixin


class PurchaseOrder(db.Model, TimestampMixin):
    __tablename__ = "purchase_orders"

    id = db.Column(db.String(64), primary_key=True)
    supplier_id = db.Column(db.String(32), db.ForeignKey("suppliers.id"), nullable=False)
    sku_id = db.Column(db.String(32), db.ForeignKey("skus.id"), nullable=False)
    location_id = db.Column(db.String(32), db.ForeignKey("locations.id"), nullable=False)
    order_quantity = db.Column(db.Float, nullable=False)
    received_quantity = db.Column(db.Float, default=0.0)
    expected_delivery_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(32), default="planned")
    lifecycle_status = db.Column(db.String(32), default="active")

    supplier = db.relationship("Supplier", back_populates="purchase_orders")
    sku = db.relationship("Sku", back_populates="purchase_orders")
    location = db.relationship("Location", back_populates="purchase_orders")

    def __repr__(self):
        return f"<PurchaseOrder {self.id}>"

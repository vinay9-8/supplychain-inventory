from backend.extensions import db
from backend.models.base import TimestampMixin


class SkuSupplier(db.Model, TimestampMixin):
    __tablename__ = "sku_supplier"

    sku_id = db.Column(db.String(32), db.ForeignKey("skus.id"), primary_key=True)
    supplier_id = db.Column(db.String(32), db.ForeignKey("suppliers.id"), primary_key=True)
    preferred_supplier = db.Column(db.Boolean, default=False)
    min_order_quantity = db.Column(db.Float, default=0.0)
    multi_source_approved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<SkuSupplier {self.sku_id}:{self.supplier_id}>"

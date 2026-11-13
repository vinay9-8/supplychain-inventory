from backend.extensions import db
from backend.models.base import TimestampMixin


class Inventory(db.Model, TimestampMixin):
    __tablename__ = "inventory"
    __table_args__ = (
        db.UniqueConstraint("sku_id", "location_id", name="uq_inventory_sku_location"),
    )

    id = db.Column(db.String(64), primary_key=True)
    sku_id = db.Column(db.String(32), db.ForeignKey("skus.id"), nullable=False)
    location_id = db.Column(db.String(32), db.ForeignKey("locations.id"), nullable=False)
    on_hand_quantity = db.Column(db.Float, default=0.0)
    reserved_quantity = db.Column(db.Float, default=0.0)
    in_transit_quantity = db.Column(db.Float, default=0.0)
    safety_stock = db.Column(db.Float, default=0.0)
    reorder_point = db.Column(db.Float, default=0.0)
    lifecycle_status = db.Column(db.String(32), default="active")

    sku = db.relationship("Sku", back_populates="inventory")
    location = db.relationship("Location", back_populates="inventory")
    events = db.relationship("InventoryEvent", back_populates="inventory")

    def __repr__(self):
        return f"<Inventory {self.id}>"

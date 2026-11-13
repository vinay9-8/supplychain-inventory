from backend.extensions import db
from backend.models.base import TimestampMixin


class InventoryEvent(db.Model, TimestampMixin):
    __tablename__ = "inventory_events"

    id = db.Column(db.String(64), primary_key=True)
    inventory_id = db.Column(db.String(64), db.ForeignKey("inventory.id"), nullable=False)
    event_type = db.Column(db.String(80), nullable=False)
    quantity_delta = db.Column(db.Float, default=0.0)
    previous_quantity = db.Column(db.Float, default=0.0)
    new_quantity = db.Column(db.Float, default=0.0)
    reason = db.Column(db.Text, default="")

    inventory = db.relationship("Inventory", back_populates="events")

    def __repr__(self):
        return f"<InventoryEvent {self.id}>"

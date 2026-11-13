from datetime import date

from backend.extensions import db
from backend.models.base import TimestampMixin


class LeadTime(db.Model, TimestampMixin):
    __tablename__ = "lead_times"
    __table_args__ = (
        db.UniqueConstraint(
            "supplier_id",
            "sku_id",
            "location_id",
            "effective_from",
            name="uq_lead_time_effective_start",
        ),
    )

    id = db.Column(db.String(64), primary_key=True)
    supplier_id = db.Column(db.String(32), db.ForeignKey("suppliers.id"), nullable=False)
    sku_id = db.Column(db.String(32), db.ForeignKey("skus.id"), nullable=False)
    location_id = db.Column(db.String(32), db.ForeignKey("locations.id"), nullable=False)
    lead_days = db.Column(db.Integer, nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    effective_to = db.Column(db.Date, nullable=True)
    lifecycle_status = db.Column(db.String(32), default="active")

    supplier = db.relationship("Supplier", back_populates="lead_times")
    sku = db.relationship("Sku", back_populates="lead_times")
    location = db.relationship("Location", back_populates="lead_times")

    def __repr__(self):
        return f"<LeadTime {self.id}>"

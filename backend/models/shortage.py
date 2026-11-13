from datetime import date

from backend.extensions import db
from backend.models.base import TimestampMixin


class Shortage(db.Model, TimestampMixin):
    __tablename__ = "shortages"

    id = db.Column(db.String(64), primary_key=True)
    sku_id = db.Column(db.String(32), db.ForeignKey("skus.id"), nullable=False)
    location_id = db.Column(db.String(32), db.ForeignKey("locations.id"), nullable=False)
    shortage_date = db.Column(db.Date, nullable=False)
    projected_shortage_units = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(32), default="medium")
    status = db.Column(db.String(32), default="open")
    lifecycle_status = db.Column(db.String(32), default="active")

    sku = db.relationship("Sku", back_populates="shortages")
    location = db.relationship("Location", back_populates="shortages")
    mitigation_options = db.relationship("MitigationOption", back_populates="shortage")

    def __repr__(self):
        return f"<Shortage {self.id}>"

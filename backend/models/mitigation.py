from backend.extensions import db
from backend.models.base import TimestampMixin


class MitigationOption(db.Model, TimestampMixin):
    __tablename__ = "mitigation_options"

    id = db.Column(db.String(64), primary_key=True)
    shortage_id = db.Column(db.String(64), db.ForeignKey("shortages.id"), nullable=False)
    mitigation_type = db.Column(db.String(80), nullable=False)
    action_description = db.Column(db.Text, nullable=False)
    recommended_quantity = db.Column(db.Float, default=0.0)
    cost_estimate = db.Column(db.Float, default=0.0)
    impact_score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(32), default="recommended")

    shortage = db.relationship("Shortage", back_populates="mitigation_options")

    def __repr__(self):
        return f"<MitigationOption {self.id}>"

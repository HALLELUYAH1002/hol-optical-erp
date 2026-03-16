from app.extensions import db
from .base import TimestampMixin


class Supplier(db.Model, TimestampMixin):
    __tablename__ = "suppliers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    contact_person = db.Column(db.String(150))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255))
    note = db.Column(db.Text)

from app.extensions import db
from .base import TimestampMixin


class Customer(db.Model, TimestampMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(40), unique=True, index=True)
    full_name = db.Column(db.String(150), nullable=False, index=True)
    phone = db.Column(db.String(30), index=True)
    whatsapp = db.Column(db.String(30))
    address = db.Column(db.String(255))
    gender = db.Column(db.String(20))
    occupation = db.Column(db.String(120))
    customer_type = db.Column(db.String(30), default='Retail')
    notes = db.Column(db.Text)

    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    branch = db.relationship('Branch', backref='customers')

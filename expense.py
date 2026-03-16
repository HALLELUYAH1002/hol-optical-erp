from app.extensions import db
from .base import TimestampMixin


class Expense(db.Model, TimestampMixin):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), default='General')
    amount = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    note = db.Column(db.Text)

    branch = db.relationship('Branch', backref='expenses')

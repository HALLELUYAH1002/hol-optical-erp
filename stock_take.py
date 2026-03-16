from app.extensions import db
from .base import TimestampMixin


class StockTakeSession(db.Model, TimestampMixin):
    __tablename__ = "stock_take_sessions"
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    expected_qty = db.Column(db.Integer, nullable=False)
    counted_qty = db.Column(db.Integer, nullable=False)
    variance = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    branch = db.relationship('Branch', backref='stock_take_sessions')
    user = db.relationship('User', backref='stock_take_sessions')

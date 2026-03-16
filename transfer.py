from app.extensions import db
from .base import TimestampMixin


class StockTransfer(db.Model, TimestampMixin):
    __tablename__ = 'stock_transfers'
    id = db.Column(db.Integer, primary_key=True)
    transfer_no = db.Column(db.String(50), unique=True, nullable=False)
    from_branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    to_branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(30), default='Pending')
    note = db.Column(db.Text)

    from_branch = db.relationship('Branch', foreign_keys=[from_branch_id], backref='outgoing_transfers')
    to_branch = db.relationship('Branch', foreign_keys=[to_branch_id], backref='incoming_transfers')
    requester = db.relationship('User', foreign_keys=[requested_by], backref='requested_transfers')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_transfers')


class StockTransferItem(db.Model, TimestampMixin):
    __tablename__ = 'stock_transfer_items'
    id = db.Column(db.Integer, primary_key=True)
    stock_transfer_id = db.Column(db.Integer, db.ForeignKey('stock_transfers.id'), nullable=False)
    item_type = db.Column(db.String(30), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    lens_power_stock_id = db.Column(db.Integer, db.ForeignKey('lens_power_stock.id'))
    quantity = db.Column(db.Integer, nullable=False)
    received_quantity = db.Column(db.Integer, default=0)

    transfer = db.relationship('StockTransfer', backref='items')
    product = db.relationship('Product', backref='transfer_items')
    lens_power = db.relationship('LensPowerStock', backref='transfer_items')

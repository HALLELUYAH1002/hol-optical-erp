from app.extensions import db
from .base import TimestampMixin


class Purchase(db.Model, TimestampMixin):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Numeric(12,2), default=0, nullable=False)
    note = db.Column(db.Text)

    supplier = db.relationship('Supplier', backref='purchases')
    branch = db.relationship('Branch', backref='purchases')
    user = db.relationship('User', backref='purchases')


class PurchaseItem(db.Model, TimestampMixin):
    __tablename__ = "purchase_items"
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_cost = db.Column(db.Numeric(12,2), default=0, nullable=False)
    total_cost = db.Column(db.Numeric(12,2), default=0, nullable=False)

    purchase = db.relationship('Purchase', backref='items')
    product = db.relationship('Product', backref='purchase_items')

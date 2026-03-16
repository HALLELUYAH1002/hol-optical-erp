from app.extensions import db
from .base import TimestampMixin


class Sale(db.Model, TimestampMixin):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subtotal = db.Column(db.Numeric(12, 2), default=0)
    discount = db.Column(db.Numeric(12, 2), default=0)
    total = db.Column(db.Numeric(12, 2), default=0)
    amount_paid = db.Column(db.Numeric(12, 2), default=0)
    balance = db.Column(db.Numeric(12, 2), default=0)
    payment_method = db.Column(db.String(30), default='Cash')
    status = db.Column(db.String(30), default='Completed')
    notes = db.Column(db.Text)

    customer = db.relationship('Customer', backref='sales')
    branch = db.relationship('Branch', backref='sales')
    user = db.relationship('User', backref='sales')


class SaleItem(db.Model, TimestampMixin):
    __tablename__ = 'sale_items'
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    item_type = db.Column(db.String(30), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    lens_power_stock_id = db.Column(db.Integer, db.ForeignKey('lens_power_stock.id'))
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), default=0)
    total_price = db.Column(db.Numeric(12, 2), default=0)
    lens_sph = db.Column(db.String(20))
    lens_cyl = db.Column(db.String(20))
    lens_axis = db.Column(db.String(20))
    lens_add = db.Column(db.String(20))

    sale = db.relationship('Sale', backref='items')

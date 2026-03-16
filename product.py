from app.extensions import db
from .base import TimestampMixin


class ProductCategory(db.Model, TimestampMixin):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class Product(db.Model, TimestampMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(50), unique=True, index=True)
    barcode = db.Column(db.String(50), index=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    brand = db.Column(db.String(80))
    model = db.Column(db.String(80))
    color = db.Column(db.String(50))
    size = db.Column(db.String(50))
    supplier_name = db.Column(db.String(120))
    cost_price = db.Column(db.Numeric(12, 2), default=0)
    retail_price = db.Column(db.Numeric(12, 2), default=0)
    wholesale_price = db.Column(db.Numeric(12, 2), default=0)
    reorder_level = db.Column(db.Integer, default=0)
    image_path = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    category = db.relationship('ProductCategory', backref='products')


class ProductStock(db.Model, TimestampMixin):
    __tablename__ = 'product_stock'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)

    product = db.relationship('Product', backref='stock_rows')
    branch = db.relationship('Branch', backref='product_stock_rows')

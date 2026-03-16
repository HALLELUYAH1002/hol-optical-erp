from app.extensions import db
from .base import TimestampMixin


class LensCatalog(db.Model, TimestampMixin):
    __tablename__ = 'lens_catalog'
    id = db.Column(db.Integer, primary_key=True)
    lens_family = db.Column(db.String(120), nullable=False, index=True)
    lens_type = db.Column(db.String(120), nullable=False)
    index_name = db.Column(db.String(50))
    coating = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class LensPowerStock(db.Model, TimestampMixin):
    __tablename__ = 'lens_power_stock'
    id = db.Column(db.Integer, primary_key=True)
    lens_catalog_id = db.Column(db.Integer, db.ForeignKey('lens_catalog.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    sph = db.Column(db.String(20), nullable=False, index=True)
    cyl = db.Column(db.String(20), default='0.00')
    axis = db.Column(db.String(20))
    add_power = db.Column(db.String(20))
    quantity = db.Column(db.Integer, default=0, nullable=False)
    cost_price = db.Column(db.Numeric(12, 2), default=0)
    retail_price = db.Column(db.Numeric(12, 2), default=0)
    wholesale_price = db.Column(db.Numeric(12, 2), default=0)
    reorder_level = db.Column(db.Integer, default=0)
    batch_no = db.Column(db.String(80))

    catalog = db.relationship('LensCatalog', backref='power_rows')
    branch = db.relationship('Branch', backref='lens_power_rows')

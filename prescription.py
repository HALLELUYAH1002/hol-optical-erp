from app.extensions import db
from .base import TimestampMixin


class Prescription(db.Model, TimestampMixin):
    __tablename__ = 'prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    optician_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    od_sph = db.Column(db.String(20))
    od_cyl = db.Column(db.String(20))
    od_axis = db.Column(db.String(20))
    os_sph = db.Column(db.String(20))
    os_cyl = db.Column(db.String(20))
    os_axis = db.Column(db.String(20))
    add_power = db.Column(db.String(20))
    pd = db.Column(db.String(20))
    segment_height = db.Column(db.String(20))
    prism = db.Column(db.String(20))
    complaint = db.Column(db.Text)
    remarks = db.Column(db.Text)
    recommended_lens_type = db.Column(db.String(120))

    customer = db.relationship('Customer', backref='prescriptions')

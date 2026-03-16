from app.extensions import db
from .base import TimestampMixin


class LabJob(db.Model, TimestampMixin):
    __tablename__ = 'lab_jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_no = db.Column(db.String(50), unique=True, nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    frame_description = db.Column(db.String(255))
    lens_description = db.Column(db.String(255))
    status = db.Column(db.String(30), default='New Order', nullable=False)
    priority = db.Column(db.String(20), default='Normal')
    notes = db.Column(db.Text)

    sale = db.relationship('Sale', backref='lab_jobs')
    customer = db.relationship('Customer', backref='lab_jobs')
    prescription = db.relationship('Prescription', backref='lab_jobs')
    branch = db.relationship('Branch', backref='lab_jobs')
    technician = db.relationship('User', backref='lab_jobs')

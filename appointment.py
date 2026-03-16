
from app.extensions import db
from .base import TimestampMixin


class Appointment(db.Model, TimestampMixin):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    appointment_type = db.Column(db.String(50), default='Review', nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Scheduled', nullable=False)
    note = db.Column(db.Text)

    customer = db.relationship('Customer', backref='appointments')
    branch = db.relationship('Branch', backref='appointments')
    creator = db.relationship('User', backref='appointments_created')

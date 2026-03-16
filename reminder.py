from app.extensions import db
from .base import TimestampMixin


class Reminder(db.Model, TimestampMixin):
    __tablename__ = "reminders"
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    lab_job_id = db.Column(db.Integer, db.ForeignKey('lab_jobs.id'))
    reminder_type = db.Column(db.String(50), default='General', nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='Open', nullable=False)

    branch = db.relationship('Branch', backref='reminders')
    customer = db.relationship('Customer', backref='reminders')
    lab_job = db.relationship('LabJob', backref='reminders')

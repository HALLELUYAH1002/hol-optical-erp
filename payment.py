from app.extensions import db
from .base import TimestampMixin


class Payment(db.Model, TimestampMixin):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    received_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(12, 2), default=0)
    payment_method = db.Column(db.String(30), default='Cash')
    reference_no = db.Column(db.String(80))
    note = db.Column(db.Text)

    sale = db.relationship('Sale', backref='payments')
    customer = db.relationship('Customer', backref='payments')
    branch = db.relationship('Branch', backref='payments')
    receiver = db.relationship('User', backref='received_payments')


class Debtor(db.Model, TimestampMixin):
    __tablename__ = 'debtors'
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    total_bill = db.Column(db.Numeric(12, 2), default=0)
    amount_paid = db.Column(db.Numeric(12, 2), default=0)
    balance = db.Column(db.Numeric(12, 2), default=0)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(30), default='Open')

    sale = db.relationship('Sale', backref=db.backref('debtor', uselist=False))
    customer = db.relationship('Customer', backref='debtor_rows')
    branch = db.relationship('Branch', backref='debtors')

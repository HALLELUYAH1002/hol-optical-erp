from decimal import Decimal
from app.extensions import db
from app.models import Debtor, Payment


def get_open_debtors(branch_id=None):
    q = Debtor.query.filter(Debtor.balance > 0)
    if branch_id:
        q = q.filter_by(branch_id=branch_id)
    return q.order_by(Debtor.created_at.desc()).all()


def record_payment_for_debtor(debtor, amount, payment_method='Cash', received_by=None, reference_no='', note=''):
    amount = Decimal(str(amount or 0))
    if amount <= 0:
        raise ValueError('Payment amount must be greater than zero.')
    if amount > Decimal(str(debtor.balance)):
        raise ValueError('Payment cannot be greater than the outstanding balance.')

    payment = Payment(
        sale_id=debtor.sale_id,
        customer_id=debtor.customer_id,
        branch_id=debtor.branch_id,
        received_by=received_by.id if received_by else debtor.sale.user_id,
        amount=amount,
        payment_method=payment_method or 'Cash',
        reference_no=reference_no or None,
        note=note or None,
    )
    db.session.add(payment)

    debtor.amount_paid = Decimal(str(debtor.amount_paid)) + amount
    debtor.balance = Decimal(str(debtor.balance)) - amount
    debtor.status = 'Paid' if debtor.balance <= 0 else 'Open'

    sale = debtor.sale
    sale.amount_paid = Decimal(str(sale.amount_paid)) + amount
    sale.balance = Decimal(str(sale.balance)) - amount
    if sale.balance <= 0:
        sale.status = 'Paid'

    db.session.commit()
    return payment

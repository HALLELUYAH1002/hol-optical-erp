from decimal import Decimal
from app.extensions import db
from app.models import Debtor, Payment, ProductStock, Sale, SaleItem, LensPowerStock


class InsufficientStockError(Exception):
    pass


def create_sale(invoice_no, customer, branch, user, items, amount_paid=0, discount=0, payment_method='Cash', notes=''):
    amount_paid = Decimal(str(amount_paid or 0))
    discount = Decimal(str(discount or 0))
    subtotal = sum(Decimal(str(item['unit_price'])) * int(item.get('quantity', 1)) for item in items)
    total = subtotal - discount
    balance = total - amount_paid

    sale = Sale(
        invoice_no=invoice_no, customer=customer, branch=branch, user=user,
        subtotal=subtotal, discount=discount, total=total,
        amount_paid=amount_paid, balance=balance, payment_method=payment_method, notes=notes,
        status='Paid' if balance <= 0 else 'Completed'
    )
    db.session.add(sale)
    db.session.flush()

    for row in items:
        if row['item_type'] == 'product':
            stock = ProductStock.query.filter_by(product_id=row['product_id'], branch_id=branch.id).first()
            if not stock or stock.quantity < int(row['quantity']):
                raise InsufficientStockError(f"Not enough stock for product {row['description']}")
            stock.quantity -= int(row['quantity'])
        elif row['item_type'] == 'lens':
            lens = LensPowerStock.query.get(row['lens_power_stock_id'])
            if not lens or lens.quantity < int(row['quantity']):
                raise InsufficientStockError(f"Not enough lens stock for power {row['description']}")
            lens.quantity -= int(row['quantity'])

        db.session.add(SaleItem(
            sale_id=sale.id,
            item_type=row['item_type'],
            product_id=row.get('product_id'),
            lens_power_stock_id=row.get('lens_power_stock_id'),
            description=row['description'],
            quantity=int(row.get('quantity', 1)),
            unit_price=row['unit_price'],
            total_price=Decimal(str(row['unit_price'])) * int(row.get('quantity', 1)),
            lens_sph=row.get('lens_sph'),
            lens_cyl=row.get('lens_cyl'),
            lens_axis=row.get('lens_axis'),
            lens_add=row.get('lens_add'),
        ))

    if amount_paid > 0:
        db.session.add(Payment(
            sale_id=sale.id,
            customer_id=customer.id,
            branch_id=branch.id,
            received_by=user.id,
            amount=amount_paid,
            payment_method=payment_method or 'Cash',
            note='Initial payment recorded during sale creation.',
        ))

    if balance > 0:
        db.session.add(Debtor(
            sale_id=sale.id, customer_id=customer.id, branch_id=branch.id,
            total_bill=total, amount_paid=amount_paid, balance=balance, status='Open'
        ))

    db.session.commit()
    return sale

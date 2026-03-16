from decimal import Decimal
from sqlalchemy import func
from app.models import Branch, Debtor, Expense, LensPowerStock, Payment, ProductStock, Sale, SaleItem, Product, LensCatalog


def _sum_or_zero(value):
    return value or Decimal('0')


def calculate_cost_of_goods(branch_id=None):
    product_rows = (
        SaleItem.query.join(Product, SaleItem.product_id == Product.id)
        .with_entities(func.coalesce(func.sum(SaleItem.quantity * Product.cost_price), 0))
        .filter(SaleItem.item_type == 'product')
    )
    lens_rows = (
        SaleItem.query.join(LensPowerStock, SaleItem.lens_power_stock_id == LensPowerStock.id)
        .with_entities(func.coalesce(func.sum(SaleItem.quantity * LensPowerStock.cost_price), 0))
        .filter(SaleItem.item_type == 'lens')
    )
    if branch_id:
        product_rows = product_rows.join(Sale, Sale.id == SaleItem.sale_id).filter(Sale.branch_id == branch_id)
        lens_rows = lens_rows.join(Sale, Sale.id == SaleItem.sale_id).filter(Sale.branch_id == branch_id)
    return _sum_or_zero(product_rows.scalar()) + _sum_or_zero(lens_rows.scalar())


def get_report_summary():
    sales_total = _sum_or_zero(Sale.query.with_entities(func.coalesce(func.sum(Sale.total), 0)).scalar())
    payments_total = _sum_or_zero(Payment.query.with_entities(func.coalesce(func.sum(Payment.amount), 0)).scalar())
    outstanding_total = _sum_or_zero(Debtor.query.with_entities(func.coalesce(func.sum(Debtor.balance), 0)).scalar())
    expenses_total = _sum_or_zero(Expense.query.with_entities(func.coalesce(func.sum(Expense.amount), 0)).scalar())
    cogs_total = calculate_cost_of_goods()
    gross_profit = sales_total - cogs_total
    net_profit = gross_profit - expenses_total
    return {
        "branches": Branch.query.count(),
        "sales_count": Sale.query.count(),
        "sales_total": sales_total,
        "payments_total": payments_total,
        "outstanding_total": outstanding_total,
        "product_stock_units": ProductStock.query.with_entities(func.coalesce(func.sum(ProductStock.quantity), 0)).scalar() or 0,
        "lens_stock_units": LensPowerStock.query.with_entities(func.coalesce(func.sum(LensPowerStock.quantity), 0)).scalar() or 0,
        "expenses_total": expenses_total,
        "cogs_total": cogs_total,
        "gross_profit": gross_profit,
        "net_profit": net_profit,
    }


def get_sales_by_branch():
    rows = (
        Branch.query
        .outerjoin(Sale, Sale.branch_id == Branch.id)
        .with_entities(Branch.name, func.count(Sale.id), func.coalesce(func.sum(Sale.total), 0))
        .group_by(Branch.id, Branch.name)
        .order_by(Branch.name.asc())
        .all()
    )
    return rows


def get_debtors_by_branch():
    rows = (
        Branch.query
        .outerjoin(Debtor, Debtor.branch_id == Branch.id)
        .with_entities(Branch.name, func.count(Debtor.id), func.coalesce(func.sum(Debtor.balance), 0))
        .group_by(Branch.id, Branch.name)
        .order_by(Branch.name.asc())
        .all()
    )
    return rows


def get_inventory_by_branch():
    rows = (
        Branch.query
        .outerjoin(ProductStock, ProductStock.branch_id == Branch.id)
        .outerjoin(LensPowerStock, LensPowerStock.branch_id == Branch.id)
        .with_entities(
            Branch.name,
            func.coalesce(func.sum(ProductStock.quantity), 0),
            func.coalesce(func.sum(LensPowerStock.quantity), 0),
        )
        .group_by(Branch.id, Branch.name)
        .order_by(Branch.name.asc())
        .all()
    )
    return rows


def get_expenses_by_branch():
    rows = (
        Branch.query
        .outerjoin(Expense, Expense.branch_id == Branch.id)
        .with_entities(Branch.name, func.count(Expense.id), func.coalesce(func.sum(Expense.amount), 0))
        .group_by(Branch.id, Branch.name)
        .order_by(Branch.name.asc())
        .all()
    )
    return rows


def get_profit_by_branch():
    results = []
    for branch in Branch.query.order_by(Branch.name.asc()).all():
        sales_total = _sum_or_zero(Sale.query.filter_by(branch_id=branch.id).with_entities(func.coalesce(func.sum(Sale.total), 0)).scalar())
        expenses_total = _sum_or_zero(Expense.query.filter_by(branch_id=branch.id).with_entities(func.coalesce(func.sum(Expense.amount), 0)).scalar())
        cogs_total = calculate_cost_of_goods(branch.id)
        gross_profit = sales_total - cogs_total
        net_profit = gross_profit - expenses_total
        results.append({
            'branch_name': branch.name,
            'sales_total': sales_total,
            'cogs_total': cogs_total,
            'expenses_total': expenses_total,
            'gross_profit': gross_profit,
            'net_profit': net_profit,
        })
    return results

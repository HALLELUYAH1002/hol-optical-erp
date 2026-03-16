from datetime import date
from sqlalchemy import func
from app.models import Branch, Debtor, LabJob, Payment, ProductStock, Reminder, Sale, User


def get_dashboard_summary(branch_id=None):
    sale_q = Sale.query
    debtor_q = Debtor.query
    stock_q = ProductStock.query
    job_q = LabJob.query
    payment_q = Payment.query

    if branch_id:
        sale_q = sale_q.filter_by(branch_id=branch_id)
        debtor_q = debtor_q.filter_by(branch_id=branch_id)
        stock_q = stock_q.filter_by(branch_id=branch_id)
        job_q = job_q.filter_by(branch_id=branch_id)
        payment_q = payment_q.filter_by(branch_id=branch_id)

    today = date.today()
    sales_today_q = sale_q.filter(func.date(Sale.created_at) == today)
    payments_today_q = payment_q.filter(func.date(Payment.created_at) == today)

    sales_total = sale_q.with_entities(func.coalesce(func.sum(Sale.total), 0)).scalar() or 0
    debt_total = debtor_q.with_entities(func.coalesce(func.sum(Debtor.balance), 0)).scalar() or 0
    today_total = sales_today_q.with_entities(func.coalesce(func.sum(Sale.total), 0)).scalar() or 0
    today_paid = payments_today_q.with_entities(func.coalesce(func.sum(Payment.amount), 0)).scalar() or 0

    return {
        'sales_count': sale_q.count(),
        'sales_total': sales_total,
        'today_sales_count': sales_today_q.count(),
        'today_sales_total': today_total,
        'today_collections_total': today_paid,
        'outstanding_count': debtor_q.filter(Debtor.balance > 0).count(),
        'outstanding_total': debt_total,
        'low_stock_count': stock_q.filter(ProductStock.quantity <= 2).count(),
        'pending_jobs': job_q.filter(LabJob.status.notin_(['Delivered', 'Ready'])) .count(),
        'ready_jobs': job_q.filter(LabJob.status == 'Ready').count(),
        'reminders_due': Reminder.query.filter(Reminder.status == 'Open', Reminder.branch_id == branch_id, Reminder.due_date <= today).count() if branch_id else Reminder.query.filter(Reminder.status == 'Open', Reminder.due_date <= today).count(),
    }


def get_recent_sales(branch_id=None, limit=8):
    q = Sale.query
    if branch_id:
        q = q.filter_by(branch_id=branch_id)
    return q.order_by(Sale.created_at.desc()).limit(limit).all()


def get_ready_jobs(branch_id=None, limit=8):
    q = LabJob.query.filter(LabJob.status == 'Ready')
    if branch_id:
        q = q.filter_by(branch_id=branch_id)
    return q.order_by(LabJob.created_at.desc()).limit(limit).all()


def get_staff_performance(branch_id=None, limit=8):
    q = (
        Sale.query.join(User, Sale.user_id == User.id)
        .outerjoin(Branch, User.branch_id == Branch.id)
        .with_entities(
            User.full_name.label('staff_name'),
            Branch.name.label('branch_name'),
            func.count(Sale.id).label('sales_count'),
            func.coalesce(func.sum(Sale.total), 0).label('sales_total'),
            func.coalesce(func.avg(Sale.total), 0).label('avg_ticket'),
        )
        .group_by(User.id, User.full_name, Branch.name)
        .order_by(func.coalesce(func.sum(Sale.total), 0).desc())
    )
    if branch_id:
        q = q.filter(Sale.branch_id == branch_id)
    return q.limit(limit).all()


from datetime import date, timedelta


def get_due_reminders(branch_id=None, limit=8):
    q = Reminder.query.filter(Reminder.status == 'Open', Reminder.due_date <= date.today() + timedelta(days=7))
    if branch_id:
        q = q.filter_by(branch_id=branch_id)
    return q.order_by(Reminder.due_date.asc()).limit(limit).all()

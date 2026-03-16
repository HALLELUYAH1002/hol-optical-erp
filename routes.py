
from datetime import datetime, date
from decimal import Decimal
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.extensions import db
from app.models import Appointment, Customer, Debtor, Expense, LabJob, LensPowerStock, Product, ProductStock, Purchase, PurchaseItem, Reminder, Supplier
from app.services.report_service import get_debtors_by_branch, get_expenses_by_branch, get_inventory_by_branch, get_profit_by_branch, get_report_summary, get_sales_by_branch
from app.services.dashboard_service import get_staff_performance
from app.utils.permissions import manager_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
@manager_required
def index():
    upcoming = Appointment.query.filter_by(branch_id=current_user.branch_id).filter(Appointment.status.in_(['Scheduled','Confirmed'])).order_by(Appointment.appointment_date.asc()).limit(8).all()
    return render_template(
        'admin/index.html',
        summary=get_report_summary(),
        sales_by_branch=get_sales_by_branch(),
        debtors_by_branch=get_debtors_by_branch(),
        inventory_by_branch=get_inventory_by_branch(),
        expenses_by_branch=get_expenses_by_branch(),
        profit_by_branch=get_profit_by_branch(),
        staff_performance=get_staff_performance(),
        upcoming_appointments=upcoming,
    )


@admin_bp.route('/expenses', methods=['GET', 'POST'])
@login_required
@manager_required
def expenses():
    if request.method == 'POST':
        expense = Expense(
            branch_id=current_user.branch_id,
            title=request.form['title'],
            category=request.form.get('category') or 'General',
            amount=request.form.get('amount') or 0,
            note=request.form.get('note') or None,
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense recorded successfully.', 'success')
        return redirect(url_for('admin.expenses'))
    expenses = Expense.query.filter_by(branch_id=current_user.branch_id).order_by(Expense.created_at.desc()).all()
    return render_template('admin/expenses.html', expenses=expenses)


@admin_bp.route('/expenses/<int:expense_id>/delete', methods=['POST'])
@login_required
@manager_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.branch_id != current_user.branch_id:
        flash('Not allowed.', 'danger')
        return redirect(url_for('admin.expenses'))
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.', 'success')
    return redirect(url_for('admin.expenses'))


@admin_bp.route('/suppliers', methods=['GET', 'POST'])
@login_required
@manager_required
def suppliers():
    if request.method == 'POST':
        supplier = Supplier(
            name=request.form['name'],
            contact_person=request.form.get('contact_person') or None,
            phone=request.form.get('phone') or None,
            address=request.form.get('address') or None,
            note=request.form.get('note') or None,
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier created successfully.', 'success')
        return redirect(url_for('admin.suppliers'))
    rows = Supplier.query.order_by(Supplier.name.asc()).all()
    return render_template('admin/suppliers.html', suppliers=rows)


@admin_bp.route('/suppliers/<int:supplier_id>/delete', methods=['POST'])
@login_required
@manager_required
def delete_supplier(supplier_id):
    row = Supplier.query.get_or_404(supplier_id)
    db.session.delete(row)
    db.session.commit()
    flash('Supplier deleted.', 'success')
    return redirect(url_for('admin.suppliers'))


@admin_bp.route('/purchases', methods=['GET', 'POST'])
@login_required
@manager_required
def purchases():
    if request.method == 'POST':
        supplier_id = int(request.form['supplier_id'])
        product_ids = request.form.getlist('product_id[]') or request.form.getlist('product_id')
        quantities = request.form.getlist('quantity[]') or request.form.getlist('quantity')
        unit_costs = request.form.getlist('unit_cost[]') or request.form.getlist('unit_cost')
        rows = []
        total = Decimal('0')
        for pid, qty, unit in zip(product_ids, quantities, unit_costs):
            if not pid or not qty:
                continue
            qty_i = int(qty or 0)
            unit_d = Decimal(unit or '0')
            if qty_i <= 0:
                continue
            rows.append((int(pid), qty_i, unit_d))
            total += qty_i * unit_d
        if not rows:
            flash('Add at least one purchase item.', 'danger')
            return redirect(url_for('admin.purchases'))
        purchase = Purchase(
            supplier_id=supplier_id,
            branch_id=current_user.branch_id,
            user_id=current_user.id,
            total=total,
            note=request.form.get('note') or None,
        )
        db.session.add(purchase)
        db.session.flush()
        for product_id, quantity, unit_cost in rows:
            db.session.add(PurchaseItem(purchase_id=purchase.id, product_id=product_id, quantity=quantity, unit_cost=unit_cost, total_cost=quantity * unit_cost))
            stock = ProductStock.query.filter_by(product_id=product_id, branch_id=current_user.branch_id).first()
            if not stock:
                stock = ProductStock(product_id=product_id, branch_id=current_user.branch_id, quantity=0)
                db.session.add(stock)
            stock.quantity += quantity
        db.session.commit()
        flash('Purchase recorded and stock updated.', 'success')
        return redirect(url_for('admin.purchases'))
    rows = Purchase.query.filter_by(branch_id=current_user.branch_id).order_by(Purchase.created_at.desc()).all()
    suppliers = Supplier.query.order_by(Supplier.name.asc()).all()
    products = Product.query.order_by(Product.name.asc()).all()
    return render_template('admin/purchases.html', purchases=rows, suppliers=suppliers, products=products)


@admin_bp.route('/reminders', methods=['GET', 'POST'])
@login_required
@manager_required
def reminders():
    if request.method == 'POST':
        reminder = Reminder(
            branch_id=current_user.branch_id,
            customer_id=int(request.form['customer_id']),
            lab_job_id=int(request.form['lab_job_id']) if request.form.get('lab_job_id') else None,
            reminder_type=request.form.get('reminder_type') or 'General',
            due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d').date(),
            message=request.form.get('message') or None,
            status='Open',
        )
        db.session.add(reminder)
        db.session.commit()
        flash('Reminder created successfully.', 'success')
        return redirect(url_for('admin.reminders'))
    rows = Reminder.query.filter_by(branch_id=current_user.branch_id).order_by(Reminder.due_date.asc()).all()
    customers = Customer.query.filter_by(branch_id=current_user.branch_id).order_by(Customer.full_name.asc()).all()
    jobs = LabJob.query.filter_by(branch_id=current_user.branch_id).order_by(LabJob.created_at.desc()).all()
    return render_template('admin/reminders.html', reminders=rows, customers=customers, jobs=jobs)


@admin_bp.route('/reminders/<int:reminder_id>/close', methods=['POST'])
@login_required
@manager_required
def close_reminder(reminder_id):
    row = Reminder.query.get_or_404(reminder_id)
    if row.branch_id != current_user.branch_id:
        flash('Not allowed.', 'danger')
        return redirect(url_for('admin.reminders'))
    row.status = 'Closed'
    db.session.commit()
    flash('Reminder closed.', 'success')
    return redirect(url_for('admin.reminders'))


@admin_bp.route('/reorder')
@login_required
@manager_required
def reorder():
    product_rows = ProductStock.query.filter_by(branch_id=current_user.branch_id).join(Product).filter(ProductStock.quantity <= Product.reorder_level).order_by(ProductStock.quantity.asc()).all()
    lens_rows = LensPowerStock.query.filter_by(branch_id=current_user.branch_id).filter(LensPowerStock.quantity <= LensPowerStock.reorder_level).order_by(LensPowerStock.quantity.asc()).all()
    return render_template('admin/reorder.html', product_rows=product_rows, lens_rows=lens_rows)


@admin_bp.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    if request.method == 'POST':
        row = Appointment(
            customer_id=int(request.form['customer_id']),
            branch_id=current_user.branch_id,
            created_by=current_user.id,
            title=request.form['title'],
            appointment_type=request.form.get('appointment_type') or 'Review',
            appointment_date=datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date(),
            appointment_time=request.form.get('appointment_time') or None,
            status=request.form.get('status') or 'Scheduled',
            note=request.form.get('note') or None,
        )
        db.session.add(row)
        db.session.commit()
        flash('Appointment created successfully.', 'success')
        return redirect(url_for('admin.appointments'))
    rows = Appointment.query.filter_by(branch_id=current_user.branch_id).order_by(Appointment.appointment_date.asc()).all()
    customers = Customer.query.filter_by(branch_id=current_user.branch_id).order_by(Customer.full_name.asc()).all()
    return render_template('admin/appointments.html', appointments=rows, customers=customers, today=date.today())


@admin_bp.route('/appointments/<int:appointment_id>/status', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    row = Appointment.query.get_or_404(appointment_id)
    if row.branch_id != current_user.branch_id:
        flash('Not allowed.', 'danger')
        return redirect(url_for('admin.appointments'))
    row.status = request.form.get('status') or row.status
    db.session.commit()
    flash('Appointment updated.', 'success')
    return redirect(url_for('admin.appointments'))


@admin_bp.route('/sms-center')
@login_required
def sms_center():
    due_reminders = Reminder.query.filter_by(branch_id=current_user.branch_id, status='Open').order_by(Reminder.due_date.asc()).limit(20).all()
    debtors = Debtor.query.filter_by(branch_id=current_user.branch_id, status='Open').order_by(Debtor.balance.desc()).limit(20).all()
    appointments = Appointment.query.filter_by(branch_id=current_user.branch_id).filter(Appointment.status.in_(['Scheduled', 'Confirmed'])).order_by(Appointment.appointment_date.asc()).limit(20).all()
    return render_template('admin/sms_center.html', due_reminders=due_reminders, debtors=debtors, appointments=appointments, today=date.today())

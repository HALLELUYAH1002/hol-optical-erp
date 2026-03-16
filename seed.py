from datetime import datetime
from app import create_app
from app.extensions import db
from app.models import Branch, Customer, Debtor, Expense, LensCatalog, LensPowerStock, Product, ProductCategory, ProductStock, Reminder, Role, Supplier, User
from app.config import Config


def seed_data():
    app = create_app()
    with app.app_context():
        db.create_all()

        role_names = {name: Role.query.filter_by(name=name).first() for name in ['super_admin', 'manager', 'staff', 'lab_technician', 'store_keeper']}
        for name in list(role_names):
            if not role_names[name]:
                role_names[name] = Role(name=name, description=name.replace('_', ' ').title())
                db.session.add(role_names[name])
        db.session.commit()

        branch = Branch.query.filter_by(code='MAIN').first()
        if not branch:
            branch = Branch(name='Halleluyah Optical Laboratory Main Branch', code='MAIN', address='Sobi Junction, Gambari, Ilorin, Kwara State', phone='09032123362')
            db.session.add(branch)
            db.session.commit()

        branch2 = Branch.query.filter_by(code='FAGBA').first()
        if not branch2:
            branch2 = Branch(name='Halleluyah Optical Laboratory Fagba Branch', code='FAGBA', address='Fagba Junction', phone='09030000000')
            db.session.add(branch2)
            db.session.commit()

        manager = User.query.filter_by(username='manager').first()
        if not manager:
            manager = User(username='manager', full_name='HOL Manager', role_id=role_names['manager'].id, branch_id=branch.id)
            manager.set_password(Config.DEFAULT_ADMIN_PASSWORD)
            db.session.add(manager)

        staff = User.query.filter_by(username='staff').first()
        if not staff:
            staff = User(username='staff', full_name='HOL Staff', role_id=role_names['staff'].id, branch_id=branch.id)
            staff.set_password('Staff123!')
            db.session.add(staff)
        db.session.commit()

        cat = ProductCategory.query.filter_by(name='Frames').first()
        if not cat:
            cat = ProductCategory(name='Frames', description='Optical frames')
            db.session.add(cat)
            db.session.commit()

        product = Product.query.filter_by(product_code='FRM-001').first()
        if not product:
            product = Product(product_code='FRM-001', name='Demo Frame', category_id=cat.id, retail_price=25000, wholesale_price=20000)
            db.session.add(product)
            db.session.commit()
            db.session.add(ProductStock(product_id=product.id, branch_id=branch.id, quantity=10))

        lens = LensCatalog.query.filter_by(lens_family='Single Vision White').first()
        if not lens:
            lens = LensCatalog(lens_family='Single Vision White', lens_type='SV White', coating='UC', index_name='1.56')
            db.session.add(lens)
            db.session.commit()
            db.session.add(LensPowerStock(lens_catalog_id=lens.id, branch_id=branch.id, sph='-1.00', cyl='0.00', quantity=8, retail_price=15000, wholesale_price=12000))

        customer = Customer.query.filter_by(full_name='Demo Customer').first()
        if not customer:
            customer = Customer(customer_code='CUS-001', full_name='Demo Customer', phone='08000000000', whatsapp='2348000000000', branch_id=branch.id)
            db.session.add(customer)
            db.session.commit()

        if not Expense.query.filter_by(title='Demo Electricity').first():
            db.session.add(Expense(branch_id=branch.id, title='Demo Electricity', category='Utilities', amount=5000, note='Sample expense for reports'))

        supplier = Supplier.query.filter_by(name='Demo Supplier').first()
        if not supplier:
            supplier = Supplier(name='Demo Supplier', contact_person='Supplier Rep', phone='08030000000', address='Lagos')
            db.session.add(supplier)

        if not Reminder.query.filter_by(reminder_type='Pickup').first():
            db.session.add(Reminder(branch_id=branch.id, customer_id=customer.id, reminder_type='Pickup', due_date=datetime.utcnow().date(), message='Customer order is ready for pickup', status='Open'))

        if not product.barcode:
            product.barcode = '1234567890123'
            product.cost_price = 12000

        db.session.commit()
        return True


if __name__ == '__main__':
    seed_data()
    print('Seed completed.')

from pathlib import Path
from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager
from .blueprints.auth.routes import auth_bp
from .blueprints.dashboard.routes import dashboard_bp
from .blueprints.customers.routes import customers_bp
from .blueprints.prescriptions.routes import prescriptions_bp
from .blueprints.inventory.routes import inventory_bp
from .blueprints.lens_grid.routes import lens_grid_bp
from .blueprints.sales.routes import sales_bp
from .blueprints.debtors.routes import debtors_bp
from .blueprints.lab.routes import lab_bp
from .blueprints.branches.routes import branches_bp
from .blueprints.admin.routes import admin_bp
from .utils.formatters import money
from .utils.permissions import has_role


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(prescriptions_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(lens_grid_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(debtors_bp)
    app.register_blueprint(lab_bp)
    app.register_blueprint(branches_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals():
        return {
            'money': money,
            'has_role': has_role,
        }

    @app.route('/')
    def root():
        from flask import redirect, url_for
        return redirect(url_for('dashboard.index'))

    @app.route('/health')
    def health():
        return {'status': 'ok', 'app': 'hol-optical-erp'}

    return app

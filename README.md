# Halleluyah Optical Laboratory Optical ERP Starter

This is a Flask + PostgreSQL starter scaffold for the online version of **Halleluyah Optical Laboratory**. It is structured around the 10-module Optical ERP plan:

1. Dashboard
2. Customers / Patients
3. Prescriptions
4. Products / Inventory
5. Lens Power Grid
6. Sales / POS
7. Debtors / Payments
8. Lab Jobs
9. Branches / Transfers
10. Reports / Admin

## Current foundation included
- App factory
- Environment-based config
- SQLAlchemy + Flask-Migrate
- Login-ready user model
- Branch / role / customer / product / lens / sales models
- Blueprint registration for all 10 modules
- Base layout, sidebar, dashboard cards, debtors widget
- Render deployment files
- Seed script

## Quick start (local)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
flask db init
flask db migrate -m "initial"
flask db upgrade
python seed.py
python run.py
```

## Quick start (Render)
1. Push this folder to a new GitHub repository.
2. Create a new Render Blueprint using `render.yaml`.
3. Deploy.
4. Open `/seed` once on a fresh database or run `python seed.py` through Render shell.

## Notes from your old desktop app
Your original Tkinter + SQLite app already had a `lens_powers` table, balance tracking, and detailed receipts. This scaffold preserves those ideas in web-ready models and service placeholders.


## New in Staff-Friendly Upgrade
- faster dashboard with quick actions
- quick customer add from sales page
- retail/wholesale auto pricing by customer type
- live sale totals before checkout
- product, lens, sales, and customer search filters
- branch-friendly low stock and ready-job highlights

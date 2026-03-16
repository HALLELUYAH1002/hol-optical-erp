from app.models import LensPowerStock


def get_low_stock_lenses(branch_id=None, threshold=2):
    q = LensPowerStock.query.filter(LensPowerStock.quantity <= threshold)
    if branch_id:
        q = q.filter_by(branch_id=branch_id)
    return q.order_by(LensPowerStock.sph.asc()).all()

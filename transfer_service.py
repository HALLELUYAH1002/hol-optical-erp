from app.extensions import db
from app.models import StockTransfer, StockTransferItem


def create_transfer(transfer_no, from_branch_id, to_branch_id, requested_by, items, note=''):
    transfer = StockTransfer(
        transfer_no=transfer_no, from_branch_id=from_branch_id, to_branch_id=to_branch_id,
        requested_by=requested_by, note=note
    )
    db.session.add(transfer)
    db.session.flush()
    for item in items:
        db.session.add(StockTransferItem(stock_transfer_id=transfer.id, **item))
    db.session.commit()
    return transfer

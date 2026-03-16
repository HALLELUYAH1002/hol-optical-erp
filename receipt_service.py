def build_receipt_context(sale):
    return {
        'company_name': 'Halleluyah Optical Laboratory',
        'sale': sale,
        'items': sale.items,
    }

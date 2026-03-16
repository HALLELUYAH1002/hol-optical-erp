def money(value):
    try:
        return f"₦{float(value):,.2f}"
    except Exception:
        return '₦0.00'

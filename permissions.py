from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def has_role(*role_names):
    role = getattr(getattr(current_user, "role", None), "name", None)
    return role in set(role_names)


def manager_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not has_role("manager", "super_admin"):
            flash("Manager permission required.", "danger")
            return redirect(url_for("dashboard.index"))
        return view(*args, **kwargs)
    return wrapped

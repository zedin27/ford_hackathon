"""Admin blueprint."""

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app_server import db
from app_server.auth import admin_required
from app_server.models import AppEntry, User
from app_server.forms import AdminSearchForm

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET", "POST"])
@admin_required
def admin_home():
    """Admin pannel.

    Lets Admins search for Apps and Users, and gives Admins a list of
    Apps that require approval
    """
    apps = AppEntry.query.filter_by(approved=False).limit(20)

    form = AdminSearchForm()
    results = []
    if form.validate_on_submit() and request.form["search"]:
        appResults = list(AppEntry.query.msearch(
            request.form["search"],
            fields=["id", "name", "description"]).limit(10))
        userResults = list(User.query.msearch(
            request.form["search"],
            fields=["id", "username", "email"]).limit(10))
        pushApp = False
        while appResults or userResults:
            if appResults and pushApp is True:
                results.append({"app": appResults.pop(0)})
                pushApp = False
            elif userResults:
                results.append({"user": userResults.pop(0)})
                pushApp = True
            else:
                pushApp = True

    return render_template(
        "admin_profile.html", apps=apps, form=form, results=results)


@bp.route("/app/<app_id>", methods=["GET"])
@admin_required
def admin_app_view(app_id):
    """Admin app view.

    Admin only interface for editing an AppEntry
    """
    app = AppEntry.query.get(app_id)
    if not app:
        return ("App not found", 400)
    user = User.query.get(app.dev_id)
    return render_template("admin_app_view.html", app=app, dev=user)


@bp.route("/user/<user_id>", methods=["GET"])
@admin_required
def admmin_app_view(user_id):
    """Admin user view.

    Admin only interface for editing a User
    """
    user = User.query.get(user_id)
    if not user:
        return ("User not found", 400)
    return render_template("admin_user_view.html", user=user)

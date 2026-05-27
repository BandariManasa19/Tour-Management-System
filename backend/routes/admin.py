from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.db import execute, get_all_bookings, get_all_packages, get_all_users, get_package_by_id

admin_bp = Blueprint("admin", __name__)


def admin_required(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Please log in as admin to access this page.", "warning")
            return redirect(url_for("auth.admin_login"))
        return route_func(*args, **kwargs)

    return wrapper


@admin_bp.route("/admin/packages", methods=["GET", "POST"])
@admin_required
def package_management():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        destination = request.form.get("destination", "").strip()
        category = request.form.get("category", "").strip()
        duration = int(request.form.get("duration", 3))
        price = float(request.form.get("price", 0))
        description = request.form.get("description", "").strip()
        available_slots = int(request.form.get("available_slots", 10))
        rating = float(request.form.get("rating", 4.5))
        image_url = request.form.get("image_url", "").strip()

        execute(
            "INSERT INTO tour_packages (title, destination, category, duration, price, description, available_slots, rating, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (title, destination, category, duration, price, description, available_slots, rating, image_url),
        )
        flash("Tour package added successfully.", "success")

    packages = get_all_packages()
    return render_template("admin_packages.html", packages=packages)


@admin_bp.route("/admin/packages/edit/<int:package_id>", methods=["GET", "POST"])
@admin_required
def edit_package(package_id):
    package = get_package_by_id(package_id)
    if not package:
        flash("Package not found.", "warning")
        return redirect(url_for("admin.package_management"))

    if request.method == "POST":
        execute(
            "UPDATE tour_packages SET title = ?, destination = ?, category = ?, duration = ?, price = ?, description = ?, available_slots = ?, rating = ?, image_url = ? WHERE id = ?",
            (
                request.form.get("title", "").strip(),
                request.form.get("destination", "").strip(),
                request.form.get("category", "").strip(),
                int(request.form.get("duration", 3)),
                float(request.form.get("price", 0)),
                request.form.get("description", "").strip(),
                int(request.form.get("available_slots", 10)),
                float(request.form.get("rating", 4.5)),
                request.form.get("image_url", "").strip(),
                package_id,
            ),
        )
        flash("Package updated successfully.", "success")
        return redirect(url_for("admin.package_management"))

    return render_template("admin_edit_package.html", package=package)


@admin_bp.route("/admin/packages/delete/<int:package_id>")
@admin_required
def delete_package(package_id):
    execute("DELETE FROM tour_packages WHERE id = ?", (package_id,))
    flash("Tour package removed.", "info")
    return redirect(url_for("admin.package_management"))


@admin_bp.route("/admin/users")
@admin_required
def users():
    users = get_all_users()
    return render_template("admin_users.html", users=users)


@admin_bp.route("/admin/bookings")
@admin_required
def bookings():
    bookings = get_all_bookings()
    try:
        bookings = [dict(b) for b in bookings] if bookings else []
    except Exception:
        pass
    return render_template("admin_bookings.html", bookings=bookings)

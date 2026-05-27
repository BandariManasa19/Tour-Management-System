from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.db import (
    add_review,
    cancel_booking,
    confirm_booking_payment,
    count_packages,
    create_booking,
    get_all_packages,
    get_booking_by_id,
    get_package_by_id,
    get_reviews_for_package,
    get_user_bookings,
)


tours_bp = Blueprint("tours", __name__)


def calculate_end_date(start_date, duration_days):
    if not start_date:
        return ""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    return (start_dt + timedelta(days=duration_days)).strftime("%Y-%m-%d")


@tours_bp.route("/packages")
def packages():
    search = request.args.get("q", "")
    category = request.args.get("category", "")
    destination = request.args.get("destination", "")
    budget = request.args.get("budget", type=float)
    page = request.args.get("page", 1, type=int)
    per_page = 12

    total_packages = count_packages(search=search, category=category or None, destination=destination or None, budget=budget)
    total_pages = max(1, (total_packages + per_page - 1) // per_page)
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    packages = get_all_packages(
        search=search,
        category=category or None,
        destination=destination or None,
        budget=budget,
        page=page,
        per_page=per_page,
    )
    return render_template(
        "packages.html",
        packages=packages,
        search=search,
        category=category,
        destination=destination,
        budget=budget,
        page=page,
        total_pages=total_pages,
        total_packages=total_packages,
    )


@tours_bp.route("/package/<int:package_id>", methods=["GET", "POST"])
def package_detail(package_id):
    package = get_package_by_id(package_id)
    if not package:
        flash("Package not found.", "warning")
        return redirect(url_for("tours.packages"))

    if request.method == "POST" and session.get("user_id"):
        rating = int(request.form.get("rating", 5))
        comment = request.form.get("comment", "").strip()
        add_review(package_id, session["user_id"], rating, comment)
        flash("Review submitted successfully.", "success")

    reviews = get_reviews_for_package(package_id)
    return render_template("package_detail.html", package=package, reviews=reviews)


@tours_bp.route("/book/<int:package_id>", methods=["GET", "POST"])
def book_package(package_id):
    if not session.get("user_id"):
        flash("Please log in before booking a tour.", "warning")
        return redirect(url_for("auth.login"))

    package = get_package_by_id(package_id)
    if not package:
        flash("Package not found.", "warning")
        return redirect(url_for("tours.packages"))

    booking = None
    payment_deadline = None

    if request.method == "POST":
        travel_date = request.form.get("travel_date", "").strip()
        num_people = int(request.form.get("num_people", 1))
        payment_method = request.form.get("payment_method", "Card")
        booking_notes = request.form.get("booking_notes", "").strip()

        if not travel_date:
            flash("Please choose your travel date before submitting the booking.", "warning")
            return render_template("booking.html", package=package, booking=booking, payment_deadline=payment_deadline)

        total_amount = round(float(package["price"]) * num_people, 2)
        journey_end_date = calculate_end_date(travel_date, int(package["duration"]))
        payment_deadline = (datetime.utcnow() + timedelta(minutes=5)).replace(microsecond=0).isoformat() + "Z"

        booking_id = create_booking(
            session["user_id"],
            package_id,
            travel_date,
            num_people,
            total_amount,
            payment_method,
            payment_deadline=payment_deadline,
            journey_end_date=journey_end_date,
            booking_notes=booking_notes,
        )

        booking = {
            "id": booking_id,
            "travel_date": travel_date,
            "num_people": num_people,
            "total_amount": total_amount,
            "status": "Pending",
            "payment_status": "Pending",
            "journey_end_date": journey_end_date,
        }
        flash("Booking saved. Complete your payment within 5 minutes to confirm it.", "info")

    return render_template("booking.html", package=package, booking=booking, payment_deadline=payment_deadline)


@tours_bp.route("/pay/<int:booking_id>", methods=["POST"])
def confirm_payment(booking_id):
    if not session.get("user_id"):
        flash("Please log in first.", "warning")
        return redirect(url_for("auth.login"))

    try:
        booking = get_booking_by_id(booking_id)
        if not booking or booking["user_id"] != session["user_id"]:
            flash("Booking not found.", "warning")
            return redirect(url_for("tours.booking_history"))

        confirm_booking_payment(booking_id)
        flash("Payment Confirmed Successfully.", "success")
        return redirect(url_for("tours.booking_history"))
    except Exception as exc:
        print(f"Error confirming payment: {exc}")
        flash("An error occurred while processing payment. Please try again.", "danger")
        return redirect(url_for("tours.booking_history"))


@tours_bp.route("/cancel/<int:booking_id>", methods=["POST"])
def cancel_booking_route(booking_id):
    if not session.get("user_id"):
        flash("Please log in first.", "warning")
        return redirect(url_for("auth.login"))

    booking = get_booking_by_id(booking_id)
    if not booking or booking["user_id"] != session["user_id"]:
        flash("Booking not found.", "warning")
        return redirect(url_for("tours.booking_history"))

    reason = request.form.get("cancellation_reason", "").strip()
    cancel_booking(booking_id, reason)
    flash("Booking cancelled successfully.", "info")
    return redirect(url_for("tours.booking_history"))


@tours_bp.route("/history")
def booking_history():
    if not session.get("user_id"):
        flash("Please log in to view booking history.", "warning")
        return redirect(url_for("auth.login"))

    bookings = get_user_bookings(session["user_id"])
    # Convert sqlite3.Row objects to plain dictionaries so templates can safely use dict methods
    try:
        bookings = [dict(b) for b in bookings] if bookings else []
    except Exception:
        # Fallback: if objects are already dict-like, keep as-is
        pass

    return render_template("history.html", bookings=bookings)


@tours_bp.route("/history/export")
def export_history():
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    if not session.get("user_id"):
        flash("Please log in to export your bookings.", "warning")
        return redirect(url_for("auth.login"))

    bookings = get_user_bookings(session["user_id"])
    try:
        bookings = [dict(b) for b in bookings] if bookings else []
    except Exception:
        pass
    response = None
    if bookings:
        from io import BytesIO

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("Travel Booking History", styles["Title"]), Spacer(1, 12)]

        data = [["Booking ID", "Destination", "Package", "People", "Amount", "Date"]]
        for booking in bookings:
            data.append(
                [
                    str(booking["id"]),
                    booking["destination"],
                    booking["title"],
                    str(booking["num_people"]),
                    f"₹{booking['total_amount']}",
                    booking["travel_date"],
                ]
            )

        table = Table(data, hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d6cdf")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ]
            )
        )
        story.append(table)
        doc.build(story)
        response = buffer.getvalue()

    if response is None:
        response = b"No bookings found."

    from flask import Response

    return Response(response, mimetype="application/pdf", headers={"Content-Disposition": "attachment; filename=booking_history.pdf"})

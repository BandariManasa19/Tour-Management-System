import json

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from ai.ai_itinerary import generate_itinerary
from ai.chatbot import answer_question
from ml.predictor import predict_booking
from models.db import get_destination_stats, get_dashboard_summary, get_recent_predictions, save_itinerary_history, save_prediction

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    prediction = None
    if request.method == "POST":
        features = {
            "user_budget": float(request.form.get("user_budget", 0)),
            "preferred_destination": request.form.get("preferred_destination", "Goa"),
            "trip_duration": int(request.form.get("trip_duration", 3)),
            "previous_bookings": int(request.form.get("previous_bookings", 0)),
            "user_ratings": float(request.form.get("user_ratings", 4.0)),
            "travel_season": request.form.get("travel_season", "Summer"),
            "package_category": request.form.get("package_category", "Budget"),
        }
        prediction = predict_booking(features)

        if session.get("user_id"):
            save_prediction(
                session["user_id"],
                prediction["prediction_label"],
                prediction["recommended_category"],
                prediction["confidence"],
                json.dumps(features),
            )
        flash("Prediction generated successfully.", "success")

    return render_template("recommendation.html", prediction=prediction)


@ai_bp.route("/itinerary", methods=["GET", "POST"])
def itinerary():
    plan = None
    if request.method == "POST":
        destination = request.form.get("destination", "").strip()
        days = int(request.form.get("days", 3))
        budget = float(request.form.get("budget", 5000))
        interests = request.form.get("interests", "culture").strip()
        travel_type = request.form.get("travel_type", "student")

        plan = generate_itinerary(destination, days, budget, interests, travel_type)

        if session.get("user_id"):
            save_itinerary_history(session["user_id"], destination, days, budget, interests, travel_type, plan)

        flash("Your personalized itinerary has been created.", "success")

    return render_template("itinerary.html", plan=plan)


@ai_bp.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    reply = None
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        reply = answer_question(question)
        flash("AI assistant response generated.", "info")

    return render_template("chatbot.html", reply=reply)


@ai_bp.route("/analytics")
def analytics():
    summary = get_dashboard_summary()
    destination_stats = get_destination_stats()
    recent_predictions = get_recent_predictions()
    return render_template("analytics.html", summary=summary, destination_stats=destination_stats, recent_predictions=recent_predictions)


@ai_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "user" and session.get("role") != "admin":
        flash("Please log in to view your dashboard.", "warning")
        return redirect(url_for("auth.login"))

    summary = get_dashboard_summary()
    return render_template("dashboard.html", summary=summary)


@ai_bp.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        flash("You are not authorized to access the admin dashboard.", "warning")
        return redirect(url_for("auth.admin_login"))

    summary = get_dashboard_summary()
    return render_template("admin_dashboard.html", summary=summary)

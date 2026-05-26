import os
from flask import Flask, render_template
from dotenv import load_dotenv

from models.db import init_database
from routes.auth import auth_bp
from routes.tours import tours_bp
from routes.ai import ai_bp
from routes.admin import admin_bp

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")
app.config["JSON_SORT_KEYS"] = False

# Initialize database schema and demo data at startup.
init_database()

app.register_blueprint(auth_bp)
app.register_blueprint(tours_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

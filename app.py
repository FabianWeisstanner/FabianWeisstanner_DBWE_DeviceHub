import os

from flask import Flask, render_template
from flask_login import LoginManager
from sqlalchemy import text

from extensions import db


app = Flask(__name__, static_folder=None)

database_url = os.environ.get("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL ist nicht gesetzt.")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Wird für sichere Fla benötigt
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "devicehub-development-key"
)

db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return db.session.get(User, int(user_id))


# Datenbankmodelle laden
from models import User, Device


# Tabellen anlegen, falls sie noch nicht vorhanden sind
with app.app_context():
    db.create_all()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/db-check")
def db_check():
    try:
        db.session.execute(text("SELECT 1"))
        return "PostgreSQL ist mit DeviceHub verbunden"
    except Exception:
        return "PostgreSQL-Verbindung fehlgeschlagen", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
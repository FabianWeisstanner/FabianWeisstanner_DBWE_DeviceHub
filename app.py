import os

from flask import Flask, render_template

from extensions import db


app = Flask(__name__, static_folder=None)

database_url = os.environ.get("DATABASE_URL")

if not database_url:
        raise RuntimeError("DATABASE_URL ist nicht gesetzt.")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


    # Datenbankmodelle laden
from models import User, Device


    # Tabellen anlegen, falls sie noch nicht existieren
with app.app_context():
        db.create_all()


@app.get("/")
def home():
        return render_template("index.html")


@app.get("/db-check")
def db_check():
        return "PostgreSQL ist mit DeviceHub verbunden"


if __name__ == "__main__":
        port = int(os.environ.get("PORT", "5000"))
        app.run(host="0.0.0.0", port=port)
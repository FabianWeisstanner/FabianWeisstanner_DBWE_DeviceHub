import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


db = SQLAlchemy()

app = Flask(__name__, static_folder=None)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.get("/")
def home():
        return render_template("index.html")


@app.get("/db-check")
def db_check():
        try:
            db.session.execute(text("SELECT 1"))
            return "PostgreSQL-Verbindung erfolgreich"
        except Exception:
            app.logger.exception("Datenbankverbindung fehlgeschlagen")
            return "PostgreSQL-Verbindung fehlgeschlagen", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
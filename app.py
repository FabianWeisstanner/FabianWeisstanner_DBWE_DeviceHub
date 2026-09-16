import os

from flask import (
            Flask,
            render_template,
            request,
            redirect,
            url_for,
            flash,
        )

from flask_login import (
            LoginManager,
            login_user,
            logout_user,
            login_required,
            current_user,
        )

from sqlalchemy import text

from extensions import db
from models import User, Device


app = Flask(__name__, static_folder=None)

database_url = os.environ.get("DATABASE_URL")

if not database_url:
            raise RuntimeError("DATABASE_URL ist nicht gesetzt.")


app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
            return db.session.get(User, int(user_id))


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


@app.route("/register", methods=["GET", "POST"])
def register():
            if request.method == "POST":
                username = request.form.get(
                    "username",
                    ""
                ).strip()

                email = request.form.get(
                    "email",
                    ""
                ).strip().lower()

                password = request.form.get(
                    "password",
                    ""
                )

                if not username or not email or not password:
                    flash("Bitte alle Felder ausfüllen.")
                    return redirect(
                        url_for("register")
                    )

                existing_username = User.query.filter_by(
                    username=username
                ).first()

                if existing_username:
                    flash(
                        "Dieser Benutzername ist bereits vergeben."
                    )

                    return redirect(
                        url_for("register")
                    )

                existing_email = User.query.filter_by(
                    email=email
                ).first()

                if existing_email:
                    flash(
                        "Diese E-Mail-Adresse ist bereits registriert."
                    )

                    return redirect(
                        url_for("register")
                    )

                user = User(
                    username=username,
                    email=email
                )

                user.set_password(password)

                db.session.add(user)
                db.session.commit()

                flash(
                    "Registrierung erfolgreich. "
                    "Du kannst dich jetzt anmelden."
                )

                return redirect(
                    url_for("login")
                )

            return render_template(
                "register.html"
            )


@app.route("/login", methods=["GET", "POST"])
def login():
            if current_user.is_authenticated:
                return redirect(
                    url_for("dashboard")
                )

            if request.method == "POST":
                username = request.form.get(
                    "username",
                    ""
                ).strip()

                password = request.form.get(
                    "password",
                    ""
                )

                user = User.query.filter_by(
                    username=username
                ).first()

                if user is None or not user.check_password(password):
                    flash(
                        "Benutzername oder Passwort ist falsch."
                    )

                    return redirect(
                        url_for("login")
                    )

                login_user(user)

                return redirect(
                    url_for("dashboard")
                )

            return render_template(
                "login.html"
            )


@app.get("/dashboard")
@login_required
def dashboard():
            return (
                f"Willkommen im DeviceHub, "
                f"{current_user.username}!"
            )


@app.get("/logout")
@login_required
def logout():
            logout_user()

            flash(
                "Du wurdest erfolgreich abgemeldet."
            )

            return redirect(
                url_for("login")
            )


if __name__ == "__main__":
            port = int(
                os.environ.get(
                    "PORT",
                    "5000"
                )
            )

            app.run(
                host="0.0.0.0",
                port=port
            )
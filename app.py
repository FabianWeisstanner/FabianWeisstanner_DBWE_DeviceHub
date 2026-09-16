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

@app.get("/devices")
@login_required
def devices():
        all_devices = Device.query.order_by(
            Device.created_at.desc()
        ).all()

        return render_template(
            "devices.html",
            devices=all_devices
        )

@app.route("/devices/add", methods=["GET", "POST"])
@login_required
def add_device():
        if request.method == "POST":
            device_name = request.form.get(
                "device_name",
                ""
            ).strip()

            manufacturer = request.form.get(
                "manufacturer",
                ""
            ).strip()

            model = request.form.get(
                "model",
                ""
            ).strip()

            serial_number = request.form.get(
                "serial_number",
                ""
            ).strip()

            operating_system = request.form.get(
                "operating_system",
                ""
            ).strip()

            device_type = request.form.get(
                "device_type",
                ""
            ).strip()

            owner = request.form.get(
                "owner",
                ""
            ).strip()

            status = request.form.get(
                "status",
                ""
            ).strip()

            if not device_name or not serial_number or not status:
                flash(
                    "Gerätename, Seriennummer und Status "
                    "sind Pflichtfelder."
                )

                return redirect(
                    url_for("add_device")
                )

            existing_device = Device.query.filter_by(
                serial_number=serial_number
            ).first()

            if existing_device:
                flash(
                    "Ein Gerät mit dieser Seriennummer "
                    "ist bereits vorhanden."
                )

                return redirect(
                    url_for("add_device")
                )

            device = Device(
                device_name=device_name,
                manufacturer=manufacturer,
                model=model,
                serial_number=serial_number,
                operating_system=operating_system,
                device_type=device_type,
                owner=owner,
                status=status,
                created_by=current_user.id
            )

            db.session.add(device)
            db.session.commit()

            flash(
                "Gerät wurde erfolgreich gespeichert."
            )

            return redirect(
                url_for("devices")
            )

        return render_template(
            "device_add.html"
        )

@app.route("/devices/<int:device_id>/edit", methods=["GET", "POST"])
@login_required
def edit_device(device_id):
        device = Device.query.get_or_404(device_id)

        if request.method == "POST":
            device_name = request.form.get(
                "device_name",
                ""
            ).strip()

            manufacturer = request.form.get(
                "manufacturer",
                ""
            ).strip()

            model = request.form.get(
                "model",
                ""
            ).strip()

            serial_number = request.form.get(
                "serial_number",
                ""
            ).strip()

            operating_system = request.form.get(
                "operating_system",
                ""
            ).strip()

            device_type = request.form.get(
                "device_type",
                ""
            ).strip()

            owner = request.form.get(
                "owner",
                ""
            ).strip()

            status = request.form.get(
                "status",
                ""
            ).strip()

            if not device_name or not serial_number or not status:
                flash(
                    "Gerätename, Seriennummer und Status "
                    "sind Pflichtfelder."
                )

                return redirect(
                    url_for(
                        "edit_device",
                        device_id=device.id
                    )
                )

            existing_device = Device.query.filter(
                Device.serial_number == serial_number,
                Device.id != device.id
            ).first()

            if existing_device:
                flash(
                    "Ein anderes Gerät mit dieser "
                    "Seriennummer ist bereits vorhanden."
                )

                return redirect(
                    url_for(
                        "edit_device",
                        device_id=device.id
                    )
                )

            device.device_name = device_name
            device.manufacturer = manufacturer
            device.model = model
            device.serial_number = serial_number
            device.operating_system = operating_system
            device.device_type = device_type
            device.owner = owner
            device.status = status

            db.session.commit()

            flash(
                "Gerät wurde erfolgreich aktualisiert."
            )

            return redirect(
                url_for("devices")
            )

        return render_template(
            "device_edit.html",
            device=device
        )

@app.post("/devices/<int:device_id>/delete")
@login_required
def delete_device(device_id):
        device = Device.query.get_or_404(device_id)

        db.session.delete(device)
        db.session.commit()

        flash("Gerät wurde erfolgreich gelöscht.")

        return redirect(
            url_for("devices")
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
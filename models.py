from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    devices = db.relationship(
        "Device",
        backref="creator",
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    device_name = db.Column(
        db.String(100),
        nullable=False
    )

    manufacturer = db.Column(db.String(100))
    model = db.Column(db.String(100))

    serial_number = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    operating_system = db.Column(db.String(100))
    device_type = db.Column(db.String(50))
    owner = db.Column(db.String(100))
    status = db.Column(db.String(50))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
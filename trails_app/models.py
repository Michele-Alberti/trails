import logging
import click
import os
from flask.cli import with_appcontext
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

log = logging.getLogger(__name__)

# Create database instance (with lazy loading)
db = SQLAlchemy()
# Check if schema exist to set understand if sqlite is in use
if os.environ.get("FLASK_TEST_DB"):
    schema = {}
    log.warning(
        "local sqlite database selected, use for testing pourposes only"
    )
else:
    schema = {"schema": "data"}


# MODELS ----------------------------------------------------------------------


class User(UserMixin, db.Model):
    __table_args__ = schema
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64), index=True, unique=False, nullable=False
    )
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    trails = db.relationship("Trail", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<UID:{self.id}>"


class Trail(db.Model):
    __table_args__ = schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    icon = db.Column(db.String(64), nullable=False)
    if schema:
        user_id = db.Column(
            db.Integer, db.ForeignKey(f"{schema['schema']}.user.id")
        )
    else:
        user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    items = db.relationship("Item", backref="trail", lazy="dynamic")

    def __repr__(self):
        return f"<TID:{self.id}, UID:{self.user_id}>"


class Item(db.Model):
    __table_args__ = schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    icon = db.Column(db.String(64), nullable=False)
    if schema:
        trail_id = db.Column(
            db.Integer, db.ForeignKey(f"{schema['schema']}.trail.id")
        )
    else:
        trail_id = db.Column(db.Integer, db.ForeignKey("trail.id"))

    def __repr__(self):
        return (
            f"<IID:{self.id}, TID:{self.trail_id}, UID:{self.trail.user_id}>"
        )

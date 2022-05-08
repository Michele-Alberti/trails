import click
from flask.cli import with_appcontext
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Create database instance (with lazy loading)
db = SQLAlchemy()

# DATABASE FUNCTIONS ----------------------------------------------------------


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    click.echo("Database initialized")


# MODELS ----------------------------------------------------------------------


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64), index=True, unique=True, nullable=False
    )
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(64))
    trails = db.relationship("Trail", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Trail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    icon = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    items = db.relationship("Item", backref="trail", lazy="dynamic")

    def __repr__(self):
        return f"<Trail: {self.name}, U_ID: {self.user_id}>"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    icon = db.Column(db.String(64), nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey("trail.id"))

    def __repr__(self):
        return f"<Item: {self.name}, T_ID: {self.trail_id}>"

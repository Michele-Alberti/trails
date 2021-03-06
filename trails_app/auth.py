import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

log = logging.getLogger(__name__)

auth = Blueprint("auth", __name__)

# LOGIN -----------------------------------------------------------------------


@auth.route("/login", defaults={"flash_type": "is-danger"})
@auth.route("/login_flash_type_<flash_type>")
def login(flash_type):
    return render_template("login.html", flash_type=flash_type)


@auth.route("/login", methods=["POST"])
def login_post():
    # Get data from form
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    # Search user
    user = User.query.filter_by(email=email).first()

    # If user exists check password
    if not user or not user.check_password(password):
        flash("User not found. Please check password and email!")
        log.info(f"{email} not found")
        return redirect(url_for("auth.login", flash_type="is-warning"))
    # If the password is correct log the user and show the profile page
    login_user(user, remember=remember)
    log.info(f"{user} log in")
    return redirect(url_for("main.profile"))


# SIGNUP ----------------------------------------------------------------------


@auth.route("/signup", defaults={"flash_type": "is-danger"})
@auth.route("/signup_flash_type_<flash_type>")
def signup(flash_type):
    return render_template("signup.html", flash_type=flash_type)


@auth.route("/signup", methods=["POST"])
def signup_post():
    # Read user data
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    # Check if user already exists
    user = User.query.filter_by(email=email).first()

    # If exist, redirect back to signup page and prompt user
    if user:
        flash("Email address already exists!")
        log.info(f"{email} already exists")
        return redirect(url_for("auth.signup", flash_type="is-warning"))

    # Otherwise create a new user
    # Hash the password
    new_user = User(username=name, email=email)
    new_user.set_password(password)

    # Add the new user
    db.session.add(new_user)
    db.session.commit()

    flash("New account created!")
    log.info(f"{new_user} added to database")

    return redirect(url_for("auth.login", flash_type="is-success"))


# LOGOUT ----------------------------------------------------------------------


@auth.route("/logout")
@login_required
def logout():
    log.info(f"{current_user} log out")
    logout_user()
    return redirect(url_for("main.index"))

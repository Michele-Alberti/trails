import logging
from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    current_app,
    flash,
)
from flask_login import login_required, current_user
from . import db
from .models import Trail
import glob
import os

log = logging.getLogger(__name__)

main = Blueprint("main", __name__)

# MAIN PROFILE ----------------------------------------------------------------


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    # Get icon names
    icon_names = glob.glob(
        os.path.join(current_app.static_folder, "images", "mountains", "*.png")
    )
    icons = [os.path.basename(icon) for icon in icon_names]

    # Find existing trails
    trails = Trail.query.filter(Trail.user_id == current_user.id)

    return render_template(
        "profile.html",
        username=current_user.username,
        trails=trails,
        icons=icons,
    )


@main.route("/profile", methods=["POST"])
@login_required
def profile_post():
    # Get data from form
    trail_name = request.form.get("trail_name")
    icon_name = request.form.get("icon_name")

    # Add trail to database
    new_trail = Trail(
        name=trail_name, icon=icon_name, user_id=current_user.id, items=[]
    )

    # Add the new user
    db.session.add(new_trail)
    db.session.commit()

    log.info(f"{new_trail} added to database")

    return redirect(url_for("main.profile"))


# TRAIL -----------------------------------------------------------------------


@main.route("/trail/<trail_id>")
@login_required
def trail(trail_id):

    return f"<h1>You selected trail #{trail_id}</h1>"


@main.route("/trail/delete/<trail_id>")
@login_required
def delete_trail(trail_id):

    # Query for selected trail
    selected_trail = Trail.query.get(trail_id)

    # Check if selected trail exist
    if not selected_trail:
        flash("This trail does not exist!")
        log.info(f"{selected_trail} does not exist")
        return f"<h1>Not exist #{trail_id}</h1>"

    # Check if selected track belongs to the current user
    if current_user.id == selected_trail.author.id:
        # Delete
        db.session.delete(selected_trail)
        db.session.commit()
        log.info(f"{selected_trail} deleted from database")
        return redirect(url_for("main.profile"))
    else:
        # Selected trail does not belong to current user
        flash("You cannot delete this trail!")
        log.info(f"{selected_trail} cannot be deleted by {current_user}")
        return f"<h1>No auth #{trail_id}</h1>"

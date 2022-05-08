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
from .models import Trail, Item
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

    log.info(f"{new_trail} added to database by {current_user}")

    return redirect(url_for("main.profile"))


# TRAIL -----------------------------------------------------------------------


@main.route("/trail/<trail_id>")
@login_required
def trail(trail_id):

    # Get icon names
    icon_names = glob.glob(
        os.path.join(current_app.static_folder, "images", "items", "*.png")
    )
    icons = [os.path.basename(icon) for icon in icon_names]

    # Get trail
    selected_trail = Trail.query.get(trail_id)

    # Check if the query gave results
    if selected_trail:
        # Check if selected track belongs to the current user
        if current_user.id == selected_trail.author.id:
            # Find existing items
            items = selected_trail.items.all()
        else:
            # Selected trail does not belong to current user
            flash("You cannot see this trail!")
            log.info(f"{selected_trail} cannot be accessed by {current_user}")
            return redirect(url_for("main.profile"))
    else:
        # Selected trail does not belong to current user
        flash("Trail not found!")
        log.info(f"Trail with ID #{trail_id} does not exist")
        return redirect(url_for("main.profile"))

    return render_template(
        "trail.html",
        username=current_user.username,
        trail=selected_trail,
        items=items,
        icons=icons,
    )


@main.route("/trail/<trail_id>/delete")
@login_required
def delete_trail(trail_id):

    # Query for selected trail
    selected_trail = Trail.query.get(trail_id)

    # Check if selected trail exist
    if not selected_trail:
        flash("This trail does not exist!")
        log.info(f"{selected_trail} does not exist")

    # Check if selected track belongs to the current user
    if current_user.id == selected_trail.author.id:
        # Delete
        db.session.delete(selected_trail)
        db.session.commit()
        log.info(f"{selected_trail} deleted from database by {current_user}")
    else:
        # Selected trail does not belong to current user
        flash("You cannot delete this trail!")
        log.info(f"{selected_trail} cannot be deleted by {current_user}")

    return redirect(url_for("main.profile"))


@main.route("/trail/<trail_id>/add_item", methods=["POST"])
@login_required
def item_post(trail_id):

    # Query for selected trail
    selected_trail = Trail.query.get(trail_id)

    # Get data from form
    item_name = request.form.get("item_name")
    icon_name = request.form.get("icon_name")

    if current_user.id == selected_trail.author.id:
        # Add trail to database
        new_item = Item(name=item_name, icon=icon_name, trail_id=trail_id)

        # Add the new user
        db.session.add(new_item)
        db.session.commit()

        log.info(f"{new_item} added to {selected_trail} by {current_user}")
    else:
        flash("You cannot add items to this trail!")
        log.info(
            f"{new_item} cannot be added by {current_user} to {selected_trail}"
        )

    return redirect(url_for("main.trail", trail_id=trail_id))


@main.route("/item/<item_id>/delete")
@login_required
def delete_item(item_id):

    # Query for selected trail and item
    selected_item = Item.query.get(item_id)

    # Check if selected trail exist
    if not selected_item:
        flash("This item does not exist!")
        log.info(f"{selected_item} does not exist")

    # Check if selected track belongs to the current user
    if current_user.id == selected_item.trail.author.id:
        # Delete
        db.session.delete(selected_item)
        db.session.commit()
        log.info(f"{selected_item} deleted from database by {current_user}")
    else:
        # Selected trail does not belong to current user
        flash("You cannot delete this trail!")
        log.info(f"{selected_item} cannot be deleted by {current_user}")

    return redirect(url_for("main.trail", trail_id=selected_item.trail.id))

import click
import pkg_resources
from hydra import compose, initialize
from omegaconf import OmegaConf
import os
from . import create_app

# Import database object
from . import db as sql_alchemy_db
from .models import User, Trail, Item, schema

# Version
__version__ = pkg_resources.require("trails_cli")[0].version


# CLI COMMANDS ----------------------------------------------------------------


@click.group()
@click.version_option(__version__)
@click.option(
    "--sqlite-test-db",
    is_flag=True,
    help="Modifier for init and delete a local sqlite database (use for testing and run the app after creating an environment variable named FLASK_TEST_DB).",
)
@click.pass_context
def cli(ctx, sqlite_test_db):
    """Command line interface for creating a local sqlite database.
    To be used only for development purposes.
    """

    # global initialization
    initialize(config_path="conf", job_name="trails_cli")
    if sqlite_test_db:
        config = compose(config_name="config", overrides=["flask=sqlite"])
        click.secho(
            "use 'export FLASK_TEST_DB=true && trails --sqlite-test-db db init && python -m trails_app flask=sqlite server=sqlite' for running the app locally\nuse 'export FLASK_TEST_DB=true && trails --sqlite-test-db db delete && unset FLASK_TEST_DB' for deleting the sqlite database",
            fg="yellow",
        )
    else:
        config = compose(config_name="config")
    app = create_app(config)
    ctx.obj = {"app": app, "config": config}


@cli.group()
@click.pass_obj
def db(obj):
    """Manage the database."""


@db.command("init")
@click.pass_obj
def init_database(obj):
    """Initialize the database."""

    app = obj["app"]

    # Create database
    with app.app_context():
        if schema:
            sql_alchemy_db.engine.execute(
                f"CREATE SCHEMA IF NOT EXISTS {schema['schema']};"
            )
        sql_alchemy_db.create_all()

        # Create the example user
        new_user = User(username="Example User", email="example@email.com")
        new_user.set_password("example_user")
        sql_alchemy_db.session.add(new_user)
        sql_alchemy_db.session.commit()

        # Create example trail
        new_trail = Trail(
            name="Civetta", icon="grey_mountains.png", user_id=1, items=[]
        )
        sql_alchemy_db.session.add(new_trail)
        sql_alchemy_db.session.commit()

        # Create example items
        new_item = Item(name="Travel to Civetta", icon="car.png", trail_id=1)
        sql_alchemy_db.session.add(new_item)
        new_item = Item(name="Trail #15", icon="boot.png", trail_id=1)
        sql_alchemy_db.session.add(new_item)
        new_item = Item(
            name="Ferrata Nomale to Torrani", icon="rope.png", trail_id=1
        )
        sql_alchemy_db.session.add(new_item)
        new_item = Item(name="Stay at Torrani", icon="shelter.png", trail_id=1)
        sql_alchemy_db.session.add(new_item)
        new_item = Item(
            name="Path to Civetta's peak", icon="peak.png", trail_id=1
        )
        sql_alchemy_db.session.add(new_item)
        new_item = Item(
            name="Ferrata degli Alleghesi to Coldai",
            icon="boot_pickaxe.png",
            trail_id=1,
        )
        sql_alchemy_db.session.add(new_item)
        new_item = Item(name="Stay at Coldai", icon="shelter.png", trail_id=1)
        sql_alchemy_db.session.add(new_item)
        new_item = Item(name="Trail #25", icon="map.png", trail_id=1)
        sql_alchemy_db.session.add(new_item)
        new_item = Item(name="Relax", icon="canteen.png", trail_id=1)
        sql_alchemy_db.session.add(new_item)
        new_item = Item(name="Travel back home", icon="car.png", trail_id=1)
        sql_alchemy_db.session.add(new_item)
        sql_alchemy_db.session.commit()

    click.secho("Database initialized", fg="green")


@db.command("delete")
@click.confirmation_option()
@click.pass_obj
def delete_database(obj):
    """Delete the database."""

    app = obj["app"]

    try:
        with app.app_context():
            sql_alchemy_db.session.remove()
            sql_alchemy_db.drop_all()
        click.secho("Database deleted", fg="green")
    except Exception:
        # Generic error
        click.secho("Cannot delete database for unknown reason", fg="red")


def main():
    cli(auto_envvar_prefix="DATA_LOADER")


if __name__ == "__main__":
    main()

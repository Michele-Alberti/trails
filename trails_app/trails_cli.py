import click
import errno
import pkg_resources
from hydra import compose, initialize
from omegaconf import OmegaConf
import os
from . import create_app

# Import database object
from . import db as sql_alchemy_db

# Version
__version__ = pkg_resources.require("trails_cli")[0].version

# LOAD HYDRA CONFIGURATION ----------------------------------------------------

# global initialization
initialize(config_path="conf", job_name="trails_cli")
config = compose(config_name="config")
app = create_app(config)

# CLI COMMANDS ----------------------------------------------------------------


@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    """Command line interface for creating a local sqlite database.
    To be used only for development purposes.
    """


@cli.group()
@click.pass_obj
def db(config):
    """Manage the database."""


@db.command("init")
def init_database():
    """Initialize the database."""

    # Create database
    with app.app_context():
        sql_alchemy_db.create_all()

    click.secho("Database initialized", fg="green")


@db.command("delete")
@click.confirmation_option()
def delete_database():
    """Delete the database."""
    db_path = os.path.join(
        "trails_app",
        config.flask.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", ""),
    )
    print(db_path)
    try:
        os.remove(db_path)
        click.secho("Database deleted", fg="green")
    except OSError as e:
        # errno.ENOENT means "no such file or directory"
        # Re-raise if a different error is found
        if e.errno != errno.ENOENT:
            raise
        click.secho("Database not found", fg="red")


def main():
    cli(auto_envvar_prefix="DATA_LOADER")


if __name__ == "__main__":
    main()

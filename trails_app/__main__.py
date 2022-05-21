import logging
import gunicorn.app.base
import hydra
import os
from omegaconf import DictConfig
from . import create_app

log = logging.getLogger(__name__)


class GunicornApplication(gunicorn.app.base.BaseApplication):
    """
    GUnicorn app object to be used directly from python.
    Options are passed as dictionary from the Hydra configuration
    object (config.server)
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


@hydra.main(config_path="conf", config_name="config")
def run_app(config: DictConfig):

    # Call the app factory function
    log.info("calling app factory function")
    app = create_app(config)
    # Check the environment variable FLASK_ENV
    # Use a Gunicorn application instance if FLASK_ENV="production"
    # Use the development server otherwise
    environment = os.getenv("FLASK_ENV")
    if environment == "production":
        log.info("starting production server")
        options = config.server
        GunicornApplication(app, options).run()
    else:
        log.info("starting development server")
        app.run(host=config.server.host, port=config.server.port)


# Call for hydra
if __name__ == "__main__":
    run_app()

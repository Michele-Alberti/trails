import logging
import hydra
from omegaconf import DictConfig
from . import create_app

log = logging.getLogger(__name__)


@hydra.main(config_path="conf", config_name="config")
def run_app(config: DictConfig):

    log.info("calling app facory function")
    app = create_app(config)
    log.info("starting app instance")
    app.run(host=config.server.host, port=config.server.port)


# Call for hydra
if __name__ == "__main__":
    run_app()

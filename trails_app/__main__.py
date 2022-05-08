import hydra
from omegaconf import DictConfig
from . import create_app


@hydra.main(config_path="conf", config_name="config")
def run_app(config: DictConfig):
    app = create_app(config)
    app.run()


# Call for hydra
if __name__ == "__main__":
    run_app()

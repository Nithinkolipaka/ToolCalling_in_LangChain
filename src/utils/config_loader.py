import yaml
from pathlib import Path


def load_config():

    # Resolve the configuration relative to this module so it also works from notebooks/.
    project_root = Path(__file__).resolve().parents[2]

    config_path = project_root / "config" / "config.yaml"

    with open(config_path, "r") as file:
        return yaml.safe_load(file)
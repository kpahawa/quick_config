import os
from quick_config.provider_wrapper import load_config_from_path
from quick_config.validator import validate_config_dir


config = None
_env_key = 'CONFIG_DIR'


__all__ = [
    'config',
    'load_default_config',
    'setup_config_with_path',
]


def load_default_config():
    wd = os.getcwd()

    conf_dir = os.environ.get(_env_key)
    if not conf_dir:
        conf_dir = "config"

    path = os.path.join(wd, conf_dir)
    validate_config_dir(path)

    return load_config_from_path(path)


def setup_config_with_path(path: str):
    """
    sets up the config provider with an explicit path to the location of the desired directory of configs

    :param path: the location of the config directory of a project to parse and load
    """
    global config
    config = load_config_from_path(path)


if __name__ != '__main__':
    if config is None:
        config = load_default_config()


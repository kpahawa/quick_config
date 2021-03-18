from quick_config.provider import _Config


def load_config_from_path(env_path: str) -> _Config:
    return _Config(env_path)

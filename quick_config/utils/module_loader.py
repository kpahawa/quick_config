import importlib.util
from typing import Dict
from os import path


def load_env_var_by_file(file_name: str, obj_to_load: str = "ENV_VARS") -> Dict:
    module_name = path.basename(file_name).split('.')[0]  # base.py --> base
    spec = importlib.util.spec_from_file_location(module_name, file_name)
    m = spec.loader.load_module(module_name)
    return m.__getattribute__(obj_to_load)


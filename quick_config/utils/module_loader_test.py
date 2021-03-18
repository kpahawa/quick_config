import os
from quick_config.utils.module_loader import load_env_var_by_file


class TestModuleLoader:
    _base = os.path.abspath(os.path.dirname(os.getcwd()))
    _test_utils_path = os.path.join(_base, 'test_utils', 'simple_configs')

    def test_load_random_module(self):
        from quick_config.test_utils.simple_configs.rando import ENV_VARS
        loaded = load_env_var_by_file(os.path.join(self._test_utils_path, 'rando.py'))
        assert ENV_VARS == loaded

    def test_load_base_module(self):
        from quick_config.test_utils.simple_configs.base import ENV_VARS
        loaded = load_env_var_by_file(os.path.join(self._test_utils_path, 'base.py'))
        assert ENV_VARS == loaded

import os


class TestModuleLoader:
    @classmethod
    def setup_class(cls):
        os.environ.setdefault('CONFIG_DIR', 'test_utils/simple_configs')
        _base = os.path.abspath(os.path.dirname(os.getcwd()))
        cls._test_utils_path = os.path.join(_base, 'tests/test_utils/simple_configs')

    @classmethod
    def teardown_class(cls):
        os.environ.setdefault('CONFIG_DIR', None)
        from quick_config import clear_config
        clear_config()

    def test_load_random_module(self):
        from tests.test_utils.simple_configs.rando import ENV_VARS
        from quick_config.utils.module_loader import load_env_var_by_file

        loaded = load_env_var_by_file(os.path.join(self._test_utils_path, 'rando.py'))
        assert ENV_VARS == loaded

    def test_load_base_module(self):
        from tests.test_utils.simple_configs.base import ENV_VARS
        from quick_config.utils.module_loader import load_env_var_by_file

        loaded = load_env_var_by_file(os.path.join(self._test_utils_path, 'base.py'))
        assert ENV_VARS == loaded

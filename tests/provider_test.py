import pytest
import os


class TestProvider:
    _cfg = None

    @classmethod
    def setup_class(cls):
        os.environ.setdefault('environment', 'test')
        os.environ.setdefault('CONFIG_DIR', 'test_utils/simple_configs')

        from quick_config import load_config
        cls._cfg = load_config()

    @classmethod
    def teardown_class(cls):
        os.environ.setdefault('environment', None)
        from quick_config import clear_config
        clear_config()

    def test_basic_env_get(self):
        assert self._cfg.environment() == 'test'

    def test_non_existent_attr(self):
        with pytest.raises(AttributeError):
            self._cfg.non_existent()

    def test_nested_get(self):
        _dir = os.getcwd()

        _expected_db_access = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(_dir, 'db.sqlite3'),
        }

        assert self._cfg.database_access() == _expected_db_access
        assert self._cfg.engine() == 'django.db.backends.sqlite3'
        assert self._cfg.var1() == {"VAR2": {"VAR3": "some_value"}}
        assert self._cfg.var3() == "some_value"

    def test_parameterized_get(self):
        _default_value = "var not found"

        assert self._cfg.database_access("ENGINE") == 'django.db.backends.sqlite3'
        assert self._cfg.var1("VAR2", "VAR3") == "some_value"
        assert self._cfg.var1("VAR2", "var4", default=_default_value) == _default_value
        with pytest.raises(KeyError):
            self._cfg.var1("random_key")

    def test_list_accessors(self):
        assert self._cfg.my_list() == ["first", "second"]
        assert self._cfg.my_list(0) == "first"
        with pytest.raises(IndexError):
            self._cfg.my_list(100)

import os
from typing import Dict, AnyStr, Union, Any, List
import logging
from quick_config.utils.module_loader import load_env_var_by_file
from quick_config.constants import ENV_KEY, TEST_ALIASES, STG_ALIASES, PROD_ALIASES, DEV_ALIASES, BASE_LOG_FMT


class _Config:
    def __init__(self, env_path, environment_key=ENV_KEY, log_fmt=BASE_LOG_FMT):
        self._configs = {}
        self._current_env = None
        self.BASE_VARS: Dict = {}
        self.DEV_VARS: Dict = {}
        self.PROD_VARS: Dict = {}
        self.TEST_VARS: Dict = {}
        self.STAGING_VARS: Dict = {}

        if env_path is None:
            raise ValueError("path to config directory to load environment configs not given")

        self.env_path = env_path

        self._current_env = os.environ.get(environment_key, "development")
        self._base_log_format = log_fmt
        if not self._current_env:
            raise RuntimeError("No environment variable set under key {}. Please set one to continue "
                               "so configs are pulled properly".format(environment_key))

        self.__setattr__(environment_key, lambda: self._current_env)

        self.__load_configs()
        self._build_env_configs()

        # Create the logger
        self.logger = logging.getLogger()
        lvl = logging.INFO if self.is_prod() else logging.DEBUG

        self.logger.setLevel(lvl)

        # create a file handler
        file_handler = logging.FileHandler('site.log')
        file_handler.setLevel(lvl)

        # create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(lvl)
        formatter = logging.Formatter(self._base_log_format)

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def is_dev(self) -> bool:
        return self._current_env.lower() in DEV_ALIASES

    def is_prod(self) -> bool:
        return self._current_env.lower() in PROD_ALIASES

    def is_staging(self) -> bool:
        return self._current_env.lower() in STG_ALIASES

    def is_testing(self) -> bool:
        return self._current_env.lower() in TEST_ALIASES

    def get_logger(self, name=None, log_format: str = None) -> logging.Logger:
        """
        Returns a logger object that is instantiated on app init.
        :param name: an optional name for the logger. If a name is given, it should check if a logging config for
            that name exists.
        :param log_format an optional logger format to apply to the current logger
        :return: a logging object
        """
        logger = self.logger
        if name:
            logger = logging.getLogger(name)

        if log_format:
            try:
                f = logging.Formatter(log_format)
            except ValueError as ve:
                logger.error("Unable to return logger with format {}. " 
                             "Using default format in cfg instead. Error: {}".format(log_format, ve.__repr__()))
                f = logging.Formatter(self._base_log_format)

            for h in self.logger.handlers:
                h.setFormatter(f)
                logger.addHandler(h)

        return logger

    def __load_configs(self):
        """
        Loads the config directory dynamically based on the file path passed in. It will populate each
        of the vars for the respective environment based on the file name. I.e., `staging.py` will populate
        the STAGING_VARS
        """

        _, _, filenames = next(os.walk(self.env_path))
        if not filenames:
            raise RuntimeError("Unable to find any files in {}".format(self.env_path))
        for filename in filenames:
            if '.py' not in filename:
                continue

            module_name = filename.split('.')[0]
            if module_name not in ['base'] + DEV_ALIASES + STG_ALIASES + PROD_ALIASES + TEST_ALIASES:
                continue

            got_vars = load_env_var_by_file(os.path.join(self.env_path, filename))
            if module_name == 'base':
                self.BASE_VARS.update(got_vars)
            elif module_name in DEV_ALIASES:
                self.DEV_VARS.update(got_vars)
            elif module_name in STG_ALIASES:
                self.STAGING_VARS.update(got_vars)
            elif module_name in PROD_ALIASES:
                self.PROD_VARS.update(got_vars)
            elif module_name in TEST_ALIASES:
                self.TEST_VARS.update(got_vars)

    def _build_env_configs(self):
        """
        reads the base file and then based on the current environment we are in, either reads the
        development, production or (staging is optional) environment file and does a set union where everything
        in base will be replaced by it's duplicate in the specific environment file

        :return: None
        """
        configs = self.BASE_VARS.copy()
        if self.is_dev():
            configs.update(self.DEV_VARS)
        elif self.is_staging():
            configs.update(self.STAGING_VARS)
        elif self.is_prod():
            configs.update(self.PROD_VARS)
        elif self.is_testing():
            configs.update(self.TEST_VARS)
        else:
            raise RuntimeError("No staging environment vars set yet. This only supports "
                               "'development', 'production', 'staging', or 'testing'. "
                               "Did you forget to import it?")
        self._configs = configs
        self._recursive_build(self._configs)

    def _recursive_build(self, configs: Dict[AnyStr, Any]):
        """
        _recursive_build recursively sets attributes on this class instance by going down the a nested config variable
        dictionary for instance, if the configs passed in were

        ```
        {
            "config1": "value1",
            "config2": {
                "a": "v1",
            }
        }
        ```

        This method will set attributes on the class instance allowing the developer to do this:
        cfg.config1()  --> returns --> "value1"
        cfg.config2()  --> returns --> {"a": "v1"}
        cfg.a()        --> returns --> "v1"

        :param configs: the configs to read and set

        :return: None
        """
        if not isinstance(configs, dict):
            return

        for key, value in configs.items():
            fn = _build_func(value)
            self.__setattr__(key.lower(), fn)
            self._recursive_build(value)


def _build_func(value: Union[AnyStr, float, int, bool, Dict]):
    """
    Build func returns a new function whose return value is the value passed in or a function which can
    return different values for collections of configs. I.e., if a config was a list or map, the function
    will accept dynamic args to index into the collection with the name of the function being the value

    :param value: the value we wish to return

    :return: a function returning the required value
    """

    def _is_collection(v) -> bool:
        return isinstance(v, dict) or isinstance(v, list) or isinstance(v, tuple)

    def _find_inner_value(key, values, default_value):
        if not _is_collection(values):
            raise KeyError("key {} cannot be accessed since remaining values are not a collection".format(key))

        if isinstance(values, dict):
            v = values.get(key)
        elif isinstance(values, list) or isinstance(values, tuple):
            if not isinstance(key, int):
                raise KeyError("key {} is not an int but was used to "
                               "index into a list/tuple config <{}>".format(key, values))
            v = values[key]
        else:
            raise KeyError("key <{}> can't be used as an accessor because config value "
                           "<{}> is not a collection".format(key, values))
        if v is not None:
            return v

        if not default_value:
            raise KeyError("key <{}> not found in config values".format(key))

        return default_value

    def _inner(*args: List[Union[AnyStr, float, int, bool]], **kwargs: Dict):
        """
        _inner is a function which is created to allow users to query into the configs on multiple nested levels.
        it can take in any number of args and
        """
        if not _is_collection(value):
            return value

        if not args and not kwargs:
            return value

        v = None
        values = value
        args = args or []
        kwargs = kwargs or {}
        default_value = None
        if 'default' in kwargs.keys():
            default_value = kwargs['default']
            del kwargs['default']

        for key in args:
            v = _find_inner_value(key, values, default_value)
            values = v

        for _, config_key_name in kwargs.items():
            v = _find_inner_value(config_key_name, values, default_value)
            values = v

        return v

    return _inner

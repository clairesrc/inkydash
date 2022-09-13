import os
import toml


class InkyDash:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(InkyDash, cls).__new__(cls)
            cls.instance._modules = []
            cls.instance.__params = {}
        return cls.instance

    def get_config(config_path):
        # read config
        config = {}
        with open(config_path, "r") as file:
            data = file.read()
            config = toml.loads(data)
        return config

    def get_params(self):
        return self.__params

    def setup(self, config, params):
        self.__params = params

        # load modules
        modules = __import__("modules", fromlist=config["modules"])
        for i, module in enumerate(config["modules"]):
            imported_module = getattr(modules, module)
            module_config = {}
            if module in config.keys():
                module_config = config[module]
            module_default_config = {}
            if "DEFAULT_CONFIG" in dir(imported_module):
                module_default_config = imported_module.DEFAULT_CONFIG
            module_instance = imported_module.module(
                {
                    "name": imported_module.MODULE_NAME,
                    "refreshInterval": imported_module.REFRESH_INTERVAL,
                    "label": imported_module.LABEL,
                    "size": imported_module.SIZE,
                    "params": imported_module.PARAMS,
                },
                module_config,
                module_default_config,
            )
            self._modules.insert(i, module_instance)

    def render(self):
        return list(
            map(lambda module_instance: module_instance.render(), self._modules)
        )

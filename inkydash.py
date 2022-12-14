import toml


class InkyDash:
    def __init__(self, config, params):
        self.__modules = []

        # load modules
        modules = __import__("modules", fromlist=config["modules"])
        for i, module in enumerate(config["modules"]):
            imported_module = getattr(modules, module)
            imported_module_keys = dir(imported_module)
            module_config = {}
            if module in config.keys():
                module_config = config[module]
            module_default_config = {}
            module_metadata = {
                "name": imported_module.MODULE_NAME,
                "refreshInterval": imported_module.REFRESH_INTERVAL,
                "label": imported_module.LABEL,
                "params": imported_module.PARAMS,
            }
            if "SIZE" in imported_module_keys:
                module_metadata["size"] = imported_module.SIZE
            elif "WIDGETS" in imported_module_keys:
                module_metadata["widgets"] = imported_module.WIDGETS

            if "DEFAULT_CONFIG" in imported_module_keys:
                module_default_config = imported_module.DEFAULT_CONFIG
            module_instance = imported_module.module(
                params,
                module_metadata,
                module_config,
                module_default_config,
            )
            self.__modules.insert(i, module_instance)

    def get_config(config_path):
        # read config
        config = {}
        with open(config_path, "r") as file:
            data = file.read()
            config = toml.loads(data)
        return config

    def render(self):
        return list(
            map(lambda module_instance: module_instance.render(), self.__modules)
        )

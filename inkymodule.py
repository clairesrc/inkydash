from datetime import datetime, timedelta

from inkydash import InkyDash


class InkyModule:
    def __init__(self, params, module, config, default_config={}):
        self.__params = {}
        self.__state = {}

        # set module metadata
        self.__module = module

        # pass down parameters to module
        if "params" in module:
            for param in module["params"]:
                self.__params[param] = params[param]

        # fallback to default config if value is not set
        for key in default_config.keys():
            if key not in config:
                config[key] = default_config[key]
        self.__config = config

        # set last updated to yesterday so data is fetched on first render
        self.__last_updated = datetime.combine(
            datetime.now(), datetime.min.time()
        ) - timedelta(hours=24)

        # run initial setup function
        self._setup()
        return

    def __is_stale(self):
        return (
            self.__last_updated + timedelta(minutes=self.__module["refreshInterval"])
            <= datetime.now()
        )

    def __set_state(self, state):
        self.__state = state
        self.__last_updated = datetime.now()
        return

    def _get_config(self):
        return self.__config

    def _get_params(self):
        return self.__params

    def _hydrate(self):
        """Updates state"""
        return

    def _setup(self):
        """Runs once on app init"""
        return

    def render(self):
        """Builds object ready for clientside with current snapshot of state"""
        if self.__is_stale():
            self.__set_state(self._hydrate())
        result = dict()
        result.update({"data": self.__state})
        result.update(self.__module)
        del result["params"]
        return result

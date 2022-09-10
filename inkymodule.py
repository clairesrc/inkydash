from datetime import datetime, timedelta

from inkydash import InkyDash


class InkyModule:
    def __init__(self, config={}, module={}):
        self.__config = config
        self.__params = {}
        self.__module = {
            "name": module["name"],
            "refreshInterval": module["refreshInterval"],
            "label": module["label"],
            "size": module["size"],
        }
        self.__state = {}
        self.__last_updated = datetime.combine(datetime.now(), datetime.min.time())
        if "params" in module:
            app_params = InkyDash().get_params()
            for param in module["params"]:
                self.__params[param] = app_params[param]


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

    def render(self):
        """Builds object ready for clientside with current snapshot of state"""
        if self.__is_stale():
            self.__set_state(self._hydrate())
        result = dict()
        result.update({"data": self.__state})
        result.update(self.__module)
        return result

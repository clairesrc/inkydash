from datetime import datetime, timedelta

class InkyModule:
    def __init__(self, config = {}, module = {}):
        self.__config = config
        self.__module = {
            "name": module["name"],
            "refreshInterval": module["refreshInterval"],
            "label": module["label"],
            "size": module["size"]
        }
        self.__state = {}
        self.__last_updated = datetime.combine(datetime.now(), datetime.min.time())
    def __is_stale(self):
        return self.__last_updated + timedelta(minutes=self.__module["refreshInterval"]) <= datetime.now()
    def _set_state(self, state):
        self.__state = state
        self.__last_updated = datetime.now()
        return
    def _get_config(self):
        return self.__config
    def _hydrate(self):
        """Updates state
        """
        return
    def render(self):
        """Builds object ready for clientside with current snapshot of state
        """
        if self.__is_stale():
            self._hydrate()
        result = dict()
        result.update({
            "data": self.__state
        })
        result.update(self.__module)
        return result

from datetime import datetime, timedelta

from inkymodule import InkyModule

MODULE_NAME = "time"
REFRESH_INTERVAL = 1
LABEL = "TIME"
SIZE = "medium"
DEFAULT_CONFIG = {"format": "%I:%M %p"}
PARAMS = []


class module(InkyModule):
    def _hydrate(self):
        time_format = self._get_config()["format"]
        return datetime.now().strftime(time_format)

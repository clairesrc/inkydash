from datetime import datetime, timedelta

from inkymodule import InkyModule

MODULE_NAME = "time"
DEFAULT_FORMAT = "%I:%M %p"
REFRESH_INTERVAL = 1
LABEL = "TIME"
SIZE = "medium"

class module(InkyModule):
    def __init__(self, config = {}):
        if "format" not in config.keys():
            config["format"] = DEFAULT_FORMAT
        super().__init__(config, {
            "name": MODULE_NAME,
            "refreshInterval": REFRESH_INTERVAL,
            "label": LABEL,
            "size": SIZE
        })
    def _hydrate(self):
        time_format = self._get_config()["format"]
        self._set_state(datetime.now().strftime(time_format))
        return
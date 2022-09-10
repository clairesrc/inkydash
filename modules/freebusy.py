from datetime import datetime, timedelta
import os
import httplib2
from dateutil import parser
from apiclient import discovery
import datetime

import credentials
from inkymodule import InkyModule


MODULE_NAME = "freebusy"
REFRESH_INTERVAL = 4
LABEL = "MEETING STATUS"
SIZE = "large"
PARAMS = ["GOOGLE_TOKEN_FILENAME", "GOOGLE_CLIENT_SECRET_FILENAME"]


class module(InkyModule):
    def __init__(self, config={}):
        if "free_indicator" not in config.keys():
            config["free_indicator"] = "FREE"
        if "busy_indicator" not in config.keys():
            config["busy_indicator"] = "BUSY"
        if "meeting_buffer" not in config.keys():
            config["meeting_buffer"] = 0
        if "timezone" not in config.keys():
            config["timezone"] = os.getenv("TZ")
        super().__init__(
            config,
            {
                "name": MODULE_NAME,
                "refreshInterval": REFRESH_INTERVAL,
                "label": LABEL,
                "size": SIZE,
                "params": PARAMS
            },
        )

        # setup
        self.__creds = credentials.get_google_credentials(
            credentials_file=self._get_params()["GOOGLE_TOKEN_FILENAME"],
            credentials_secret=self._get_params()["GOOGLE_CLIENT_SECRET_FILENAME"],
        )

    def _hydrate(self):
        return self.__get_freebusy()

    def __get_freebusy(self):
        """Creates a Google Calendar API service object and outputs free/busy status"""
        http = self.__creds.authorize(httplib2.Http())
        service = discovery.build("calendar", "v3", http=http)
        now = datetime.datetime.now().astimezone()
        config = self._get_config()

        eventsResult = (
            service.freebusy()
            .query(
                body={
                    "timeMin": datetime.datetime.combine(
                        now, datetime.datetime.min.time()
                    )
                    .astimezone()
                    .isoformat(),
                    "timeMax": datetime.datetime.combine(
                        now, datetime.datetime.max.time()
                    )
                    .astimezone()
                    .isoformat(),
                    "timeZone": config["timezone"],
                    "items": [{"id": "primary"}],
                }
            )
            .execute()
        )
        busy = eventsResult["calendars"]["primary"]["busy"]
        if len(busy) == 0:
            return config["free_indicator"]

        event = busy[0]
        event_start = (
            parser.parse(event["start"])
            - timedelta(minutes=config["meeting_buffer"])
        ).astimezone()
        event_end = parser.parse(event["end"]).astimezone()

        if event_start <= now <= event_end:
            return config["busy_indicator"]
        else:
            return config["free_indicator"]

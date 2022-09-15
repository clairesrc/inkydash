from datetime import datetime, timedelta
import os
from dateutil import parser
from apiclient import discovery
import datetime

import credentials
from inkymodule import InkyModule


MODULE_NAME = "freebusy"
REFRESH_INTERVAL = 4
LABEL = "MEETING STATUS"
WIDGETS = [
    {"name": "freebusy", "size": "large"},
    {"name": "next", "size": "small"},
]
DEFAULT_CONFIG = {
    "free_indicator": "FREE",
    "busy_indicator": "BUSY",
    "meeting_buffer": 0,
    "timezone": os.getenv("TZ"),
}
PARAMS = ["GOOGLE_TOKEN_FILENAME", "GOOGLE_CLIENT_SECRET_FILENAME"]


class module(InkyModule):
    def _setup(self):
        self.__creds = credentials.get_google_credentials(
            token_file=self._get_params()["GOOGLE_TOKEN_FILENAME"],
            client_secrets_file=self._get_params()["GOOGLE_CLIENT_SECRET_FILENAME"],
        )

    def _hydrate(self):
        return self.__get_freebusy()

    def __get_freebusy(self):
        """Creates a Google Calendar API service object and outputs free/busy status"""
        service = discovery.build("calendar", "v3", credentials=self.__creds)
        now = datetime.datetime.now().astimezone()
        config = self._get_config()
        freebusy = config["free_indicator"]
        next = "No more meetings today"

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
        if len(busy) > 0:
            event = busy[0]
            event_start = (
                parser.parse(event["start"])
                - timedelta(minutes=config["meeting_buffer"])
            ).astimezone()
            event_end = parser.parse(event["end"]).astimezone()

            if event_start <= now <= event_end:
                freebusy = config["busy_indicator"]

        if len(busy) > 1:
            next = (
                "Next meeting \n"
                + parser.parse(busy[1]["start"]).strftime("%-I:%M %p")
                + "-"
                + parser.parse(busy[1]["end"]).strftime("%-I:%M %p")
            )

        return {"freebusy": freebusy, "next": next}

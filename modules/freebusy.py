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
LABEL = "Meeting Status"
SIZE = "large"

class module(InkyModule):
    def __init__(self, config = {}):
        if "credentials_file" not in config.keys():
            config["credentials_file"] = "/root/.credentials" + credentials.INKYDASH_GOOGLE_CREDENTIALS_FILE
        if "secret_file" not in config.keys():
            config["secret_file"] = "/inkydash/config" + credentials.CLIENT_SECRET_FILE
        if "free_indicator" not in config.keys():
            config["free_indicator"] = "FREE"
        if "busy_indicator" not in config.keys():
            config["busy_indicator"] = "BUSY"
        if "meeting_buffer" not in config.keys():
            config["meeting_buffer"] = 0
        if "timezone" not in config.keys():
            config["timezone"] = os.getenv("TZ")
        super().__init__(config, {
            "name": MODULE_NAME,
            "refreshInterval": REFRESH_INTERVAL,
            "label": LABEL,
            "size": SIZE
        })

        # setup
        self.__creds = credentials.get_google_credentials(
            credentials_file=self._get_config()["credentials_file"],
            credentials_secret=self._get_config()["secret_file"],
        )
    def _hydrate(self):
        self._set_state(self.__get_freebusy())
        return
    def __get_freebusy(self):
        """Creates a Google Calendar API service object and outputs free/busy status"""
        http = self.__creds.authorize(httplib2.Http())
        service = discovery.build("calendar", "v3", http=http)
        now = datetime.datetime.now().astimezone()

        eventsResult = (
            service.freebusy()
            .query(
                body={
                    "timeMin": datetime.datetime.combine(now, datetime.datetime.min.time())
                    .astimezone()
                    .isoformat(),
                    "timeMax": datetime.datetime.combine(now, datetime.datetime.max.time())
                    .astimezone()
                    .isoformat(),
                    "timeZone": self._get_config()["timezone"],
                    "items": [{"id": "primary"}],
                }
            )
            .execute()
        )
        busy = eventsResult["calendars"]["primary"]["busy"]
        if len(busy) == 0:
            return {"status": self._get_config()["free_indicator"], "next": False}

        event = busy[0]
        event_start = (
            parser.parse(event["start"]) - timedelta(minutes=self._get_config()["meeting_buffer"])
        ).astimezone()
        event_end = parser.parse(event["end"]).astimezone()

        if event_start <= now <= event_end:
            return {"status": self._get_config()["busy_indicator"], "next": event}
        else:
            return {"status": self._get_config()["free_indicator"], "next": event}
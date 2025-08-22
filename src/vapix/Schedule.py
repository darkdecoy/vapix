from __future__ import annotations
from typing import TYPE_CHECKING
import json
import icalendar

# Import for type hints only
if TYPE_CHECKING:
    from .VapixAPI import VapixAPI


class ScheduleEndpoint:

    def __init__(self, api: VapixAPI) -> None:

        self.api = api
        self.api.base_url = "http://" + self.api.host + "/vapix"

        self.schedules = {}

        self.get_schedules()

    def get_schedules(self):

        resp = self.api._send_request("schedule/GetScheduleInfoList")

        data = json.loads(resp)

        for schedule in data['ScheduleInfo']:

            self.schedules[schedule['Name']] = Schedule(token=schedule['token'], schedule=self)
    
    def update_schedules(self):
        self.schedules

class Schedule:

    def __init__(self, schedule: ScheduleEndpoint, token) -> None:

        self.api = schedule.api

        self.name = ""
        self.token = token
        self.description = ""
        self.attribute = []
        self.type = "addition"
        self.calendar = None

        self.get_schedule()

    def get_schedule(self):

        resp = self.api._send_request("schedule/GetSchedule", params={"Token": self.token})

        data = json.loads(resp)

        if data['Schedule'][0]['ScheduleDefinition'] != '':
            self.type = "addtion"
            schedule = data['Schedule'][0]['ScheduleDefinition']

        elif data['Schedule'][0]['ExceptionScheduleDefinition']:
            self.type = "subtraction"
            schedule = data['Schedule'][0]['ExceptionScheduleDefinition']

        self.calendar = icalendar.Calendar.from_ical(schedule)

    def add_calendar(self) -> str:

        return self.calendar.definition

from __future__ import annotations
from typing import TYPE_CHECKING
import json
import icalendar
from datetime import datetime

# Import for type hints only
if TYPE_CHECKING:
    from .device import device


class ScheduleEndpoint:

    def __init__(self, device: device) -> None:

        self.api = device.api
        self.api.base_url = "http://" + self.api.host + "/vapix"

        self.schedules = {}

        self.update_schedules()

    def update_schedules(self):

        resp = self.api._send_request("schedule/GetScheduleInfoList")

        for schedule in resp['ScheduleInfo']:

            self.schedules[schedule['Name']] = Schedule(token=schedule['token'], schedule=self)

    def set_schedule(self, name, operator="addition", schedule = "BEGIN:VCALENDAR\r\nPRODID:\r\nVERSION:2.0\r\nEND:VCALENDAR\r\n", token = "") -> None:

        if operator == "addition":
            scheduledefinition = schedule
            exceptionscheduledefinition = ""
        else:
            scheduledefinition = ""
            exceptionscheduledefinition = schedule

        resp = self.api._send_request(
            ("schedule"),
            method="POST",
            params={
                "axsch:SetSchedule": {
                    "Schedule":[
                    {
                        "Name": name,
                        "Description": "",
                        "ScheduleDefinition": scheduledefinition,
                        "ExceptionScheduleDefinition": exceptionscheduledefinition,
                        "Attribute":[],
                        "token": token
                    }
                    ]
                }
            }
        )

        self.update_schedules()

class Schedule:

    def __init__(self, schedule: ScheduleEndpoint, token = "") -> None:

        self.api = schedule.api

        self.name = ""
        self.token = token
        self.description = ""
        self.attribute = []

        self.operator = "addition"
        self.calendar = icalendar.Calendar()

        self.get_schedule()

    def get_schedule(self) -> None:

        resp = self.api._send_request("schedule/GetSchedule", params={"Token": self.token})

        self.name = resp['Schedule'][0]['Name']
        self.description = resp['Schedule'][0]['Description']
        self.attribute = resp['Schedule'][0]['Attribute']

        if len(resp['Schedule']) == 0:
            return None

        if resp['Schedule'][0]['ScheduleDefinition'] != '':
            schedule = resp['Schedule'][0]['ScheduleDefinition']

        elif resp['Schedule'][0]['ExceptionScheduleDefinition']:
            schedule = resp['Schedule'][0]['ExceptionScheduleDefinition']

        self.calendar = icalendar.Calendar.from_ical(schedule)

    def get_ical(self) -> str:

        return icalendar.Calendar.to_ical(self.calendar).decode("utf-8")

    def update_schedule(self) -> None:

        if self.operator == "addition":
            scheduledefinition = self.get_ical()
            exceptionscheduledefinition = ""
        else:
            scheduledefinition = ""
            exceptionscheduledefinition = self.get_ical()

        resp = self.api._send_request(
            ("schedule"),
            method="POST",
            params={
                "axsch:SetSchedule": {
                    "Schedule":[
                    {
                        "Name": self.name,
                        "Description": "",
                        "ScheduleDefinition": scheduledefinition,
                        "ExceptionScheduleDefinition": exceptionscheduledefinition,
                        "Attribute":[],
                        "token": self.token
                    }
                    ]
                }
            }
        )

    def add_event(self, name, start, end, rrules = "") -> None:

        event = icalendar.Event()

        event.add('summary', name)
        event.add('dtstart', start)
        event.add('dtend', end)
        event.add('dtstamp', datetime.now())

        if rrules != "":
            event.add('rrules', rrules)

        self.get_schedule()

        self.calendar.add_component(event)

        self.update_schedule()

from __future__ import annotations
from typing import TYPE_CHECKING
import json

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

        self.name = "Test Schedule"
        self.token = token
        self.description = "New Schedule"
        self.attribute = []
        self.type = "addition"
        self.calendar = ""

        self.get_schedule()

    def get_schedule(self):

        resp = self.api._send_request("schedule/GetSchedule", params={"Token": self.token})

        data = json.loads(resp)

        schedule = data['Schedule'][0]

        self.name = schedule['Name']
        self.description = schedule['Description']
        self.attribute = schedule['Attribute']

        if schedule['ScheduleDefinition'] != '':
            self.type = "addition"
            self.calendar = Calendar(definition=schedule['ScheduleDefinition'])
        elif schedule['ExceptionScheduleDefinition'] != '':
            self.type = "subtraction"
            self.calendar = Calendar(definition=schedule['ExceptionScheduleDefinition'])
        else:
            print("Invalid Schedule Definition Provided")

        self.token

    def scheduledefinition(self) -> str:

        return self.calendar.definition

class Calendar:

    def __init__(self, definition) -> None:

        self.prefix = "BEGIN:VCALENDAR\r\nPRODID:\r\nVERSION:2.0\r\n"
        self.postfix = "END:VCALENDAR\r\n"

        self.definition = definition

        self.events = {}

        self.create_events(events=self.definition.strip(self.prefix).strip(self.postfix))

    def create_events(self, events) -> None:

        name = ""

        events = events.split("\r\n")

        for event in events:

            data = event.split(":")

            match data[0]:
                case "SUMMARY":
                    name = data[1]
                    self.events[name] = Event()
                    self.events[name].summary = name
                case "DTSTART":
                    self.events[name].start_date = data[1]
                case "DTEND":
                    self.events[name].end_date = data[1]
                case "RRULE":
                    self.events[name].rrule = data[1]
                case "DTSTAMP":
                    self.events[name].dtstamp = data[1]
                case "UID":
                    self.events[name].uid = data[1]

    def update_definition(self) -> None:

        definition = self.prefix

        for name in self.events:

            definition += self.events[name].eventdefinition()

            definition += "\r\n"

        definition += self.postfix

        self.definition = definition

class Event:

    def __init__(self) -> None:

        self.summary = ""
        self.start_date = ""
        self.end_date = ""
        self.rrule = ""
        self.dtstamp = ""
        self.uid = ""

    def eventdefinition(self):

        definition = "BEGIN:VEVENT\r\nSUMMARY:" + self.summary
        
        if self.start_date != "":
            definition += "\r\nDTSTART:" + self.start_date
        
        if self.end_date != "":
            definition += "\r\nDTEND:" + self.end_date
            
        if self.rrule != "":
            definition += "\r\nRRULE:" + self.rrule
            
        if self.dtstamp != "":
            definition += "\r\nDTSTAMP:" + self.dtstamp
            
        if self.uid != "":
            definition += "\r\nUID:" + self.uid
            
        definition += "\r\nEND:VEVENT"

        return definition

from vapix.api import api
from vapix.Schedule import Schedule
import icalendar
import datetime

schedule_name = 'Another One'
name = 'GGF HR Association Monthly Meeting'
start = datetime.datetime(2025, 9, 18, 16, 0)
end = datetime.datetime(2025, 9, 18, 18, 0)

control1 = api(host="192.168.1.20", user="root", password="changem3")

control1.schedule.schedules[schedule_name].add_event(name=name, start=start, end=end)

control1.doorcontrol.doors['Door 1'].set_schedule(ScheduleToken=control1.schedule.schedules[schedule_name].token, action="Unlock")

print()

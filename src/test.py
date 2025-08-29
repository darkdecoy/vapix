from vapix.api import api
import icalendar

control1 = api(host="192.168.1.137", user="root", password="changem3")

doors = control1.doorcontrol.doors
schedules = control1.schedule.schedules

schedule_name = 'Test'

original = schedules[schedule_name].calendar

print(original)

doors['Door 1'].set_schedule(ScheduleToken="Test", action="Unlock")

print()
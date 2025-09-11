from axis_vapix.device import a1001
import datetime

schedule_name = 'Another One'
name = 'Test Meeting 1'
start = datetime.datetime(2025, 9, 18, 16, 0)
end = datetime.datetime(2025, 9, 18, 18, 0)

control1 = a1001(host="192.168.1.20", user="root", password="changem3")

control1.schedule.set_schedule(name=schedule_name, token=("manager01_" + "anotherone"))

control1.schedule.schedules[schedule_name].add_event(name=name, start=start, end=end)

control1.doorcontrol.doors['Door 1'].set_schedule(ScheduleToken=control1.schedule.schedules[schedule_name].token, action="Unlock")

print(control1.doorcontrol.doors['Door 1'].schedules)

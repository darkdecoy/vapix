from axis_vapix.device import a1001
import datetime

schedule_name = 'Another One'
token = ("manager01_" + "anotherone")
name = 'Test Meeting 1'
start = datetime.datetime(2025, 7, 18, 16, 0)
end = datetime.datetime(2025, 7, 18, 18, 0)

control1 = a1001(host="192.168.1.20", user="root", password="changem3")

control1.schedule.create_schedule(name=schedule_name, operator="addition", token=token)

for x in range(1):
    control1.schedule.schedules[token].add_event(name=(name + str(x)), start=start, end=end)

    control1.schedule.schedules[token].remove_pastevents()

control1.schedule.remove_schedule(token=token)

control1.doorcontrol.doors['Door 1'].set_unlockschedules(token=control1.schedule.schedules[token].parent, reset=False)

print(control1.doorcontrol.doors['Door 1'].unlockschedules)

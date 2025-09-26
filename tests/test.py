from axis_vapix.device import a1001
import datetime

def init():

    data = {
        "controller": {
            "host": "192.168.1.20",
            "user": "root",
            "password": "changem3",
            "doors": [{
                "name": "Door 1",
                "postfix_pattern": " %Y %m",
                "tags": ["Manager01"]}]},
        "schedule": {
            "name": 'AnotherOne',
            "token": ("manager01_" + "anotherone"),
            "tokens": list()},
        "event": {
            "name": 'Test Meeting 1',
            "starts_at": datetime.datetime(2025, 7, 18, 16, 0),
            "ends_at": datetime.datetime(2025, 7, 18, 18, 0)}}

    data["schedule"]["tokens"].append(data["schedule"]["token"])

    data["controller"]["api"] = a1001(
            host=data["controller"]["host"],
            user=data["controller"]["user"],
            password=data["controller"]["password"],
        )

    return data

def poll(controller, data):

    for token in controller["api"].schedule.schedules.keys():

        if token.split("_")[0].lower() in data["schedule"]["tokens"]:

            controller["api"].schedule.schedules[token].enabled = True

            controller["api"].schedule.schedules[token].get_schedule()

    for door in controller["doors"]:

        controller["api"].doorcontrol.doors[door["name"]].get_unlockschedules()

    data["controller"] = controller
    return data


def push(controller, data):

    events = 1

    for door in controller["doors"]:

        for tag in door["tags"]:

            for x in range(events):

                postfix = data["event"]["starts_at"].strftime(door["postfix_pattern"])
                schedule_name = tag + postfix
                schedule_token = (tag + postfix).lower().replace(" ", "_")

                if schedule_token not in controller["api"].schedule.schedules.keys():
                    controller["api"].schedule.create_schedule(
                        name=schedule_name, token=schedule_token
                    )

                controller["api"].schedule.schedules[schedule_token].add_event(
                    name=(data["event"]["name"] + str(x)), start=data["event"]["starts_at"], end=data["event"]["ends_at"]
                )

                controller["api"].doorcontrol.doors[door["name"]].set_unlockschedules(
                    token=schedule_token, reset=False
                )

    controller["api"].schedule.create_schedule(name=data["schedule"]["name"], operator="addition", token=data["schedule"]["token"])


def purge(controller):

    controller["api"].schedule.remove_pastschedules()

    print()


def main():

    data = init()

    data = poll(controller=data["controller"], data=data)

    purge(controller=data["controller"])

    push(controller=data["controller"], data=data)

    print("...Test Completed")


if __name__ == "__main__":
    main()

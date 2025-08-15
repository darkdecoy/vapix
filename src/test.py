from vapix.api import api as VapixAPI

vapix_api = VapixAPI("192.168.1.137", "root", "changem3")

doors = vapix_api.doorcontrol.get_info()

for door in doors:
    state = vapix_api.doorcontrol.update_state(token=door["token"], action="Block")

    print(state)

    state = vapix_api.doorcontrol.update_state(token=door["token"], action="Unlock")

    print(state)

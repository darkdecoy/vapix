from __future__ import annotations
from typing import TYPE_CHECKING
import json

# Import for type hints only
if TYPE_CHECKING:
    from .VapixAPI import VapixAPI


class DoorControl:

    def __init__(self, api: VapixAPI) -> None:

        self.api = api
        self.api.base_url = "http://" + self.api.host + "/vapix"

        self.doors = {}

        self.get_doors()

    def get_doors(self):
        """
        Gets the door info.

        Returns:
            list: A dictionary containing door info.
        """
        resp = self.api._send_request(
            "doorcontrol/GetDoorInfoList",
        )

        data = json.loads(resp)

        for door in data['DoorInfo']:

            self.doors[door['Name']] = Door(token=door['token'], controller=self)

class Door:

    def __init__(self, token, controller: DoorControl) -> None:

        self.controller = controller

        self.actions_table = {
            "Blocked": ("Block","DoubleLock", "Lock", "LockDown", "LockDownRelease", "LockOpen", "LockOpenRelease", "Unlock",),
            "DoubleLocked": ("Block","DoubleLock","Lock","LockDown","LockDownRelease","LockOpen","LockOpenRelease","Unlock"),
            "Locked": ("Block", "DoubleLock","Lock","LockDown", "LockDownRelease", "LockOpen", "LockOpenRelease", "Unlock",),
            "LockedDown": ("LockDown","LockDownRelease",),
            "LockedDownRelease": ("Block", "DoubleLock", "Lock", "LockDown","LockDownRelease", "LockOpen", "LockOpenRelease", "Unlock",),
            "LockedOpen": ("LockOpen", "LockOpenRelease",),
            "LockedOpenRelease": ("Block", "DoubleLock", "Lock", "LockDown", "LockOpen", "LockOpenRelease", "Unlock",),
            "Unlocked": ("Block", "DoubleLock", "Lock", "LockDown", "LockDownRelease", "LockOpen", "LockOpenRelease","Unlock",),
        }

        self.actions = ("Block","DoubleLock","Lock","LockDown","LockDownRelease","LockOpen","LockOpenRelease","Unlock")

        self.Name = ''
        self.Description = ''
        self.Capabilities = {}
        self.token = token
        
        self.DoorPhysicalState = ''
        self.Alarm = ''
        self.Mode = ''

        self.LastUpdate = True
        self.Status = 'Door Created'
        
        self.update()

    def _check_action(self, token, action) -> None:
        """
        Gets the door info.

        Returns:
            list: A dictionary containing door state info.
        """

        if action in self.actions_table[self.Mode] and self.Capabilities[action]:
            return True
        else:
            return False
    
    def _get_info(self) -> None:
        """
        Gets the door info.

        Returns:
            list: A dictionary containing door info.
        """
        resp = self.controller.api._send_request(
            "doorcontrol/GetDoorInfo",
            params={"Token": self.token},
        )

        data = json.loads(resp)

        self.Name = data['DoorInfo'][0]['Name']
        self.Description = data['DoorInfo'][0]['Description']
        self.Capabilities = data['DoorInfo'][0]['Capabilities']
        self.token = data['DoorInfo'][0]['token']

    def _get_state(self) -> None:
        """
        Gets the door info.

        Returns:
            list: A dictionary containing door state info.
        """
        resp = self.controller.api._send_request(
            "doorcontrol/GetDoorState",
            params={"Token": self.token},
        )

        data = json.loads(resp)

        self.DoorPhysicalState = data['DoorState']['DoorPhysicalState']
        self.Alarm = data['DoorState']['Alarm']
        self.Mode = data['DoorState']['DoorMode']

    def update(self) -> None:
        """
        Update Door state and info.
        """

        self._get_info()
        self._get_state()

    def set_mode(self, action) -> None:
        """
        Set Door Mode.
        """

        if action in self.actions and self._check_action(token=self.token, action=action):

            resp = self.controller.api._send_request(
                ("doorcontrol/" + action + "Door"),
                params={"Token": self.token},
            )

            self._get_state()

            if self.Mode.startswith(action):
                self.LastUpdate = True
                self.Status = "State Updated"
            else:
                self.LastUpdate = False
                self.Status = "State Not Updated"

        else:

            self.LastUpdate = False
            self.Status = "Action Not Supported"

    def set_schedule(self, ScheduleToken, action, name = "", description = "", priority = "High"):
        
        resp = self.controller.api._send_request(
            ("doorcontrol"),
            method="POST",
            params={
                "axtdc:SetDoorScheduleConfiguration": {
                    "DoorScheduleConfiguration": [
                    {
                        "token": self.token,
                        "Name": name,
                        "Description": description,
                        "DoorSchedule": [
                        {
                            "ScheduledState": [
                            {
                                "ScheduleToken": ScheduleToken,
                                "EnterAction": action
                            },
                            ],
                            "PriorityLevel": priority
                        }
                        ]
                    }
                    ]
                }
            }
        )

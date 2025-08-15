from __future__ import annotations
from typing import TYPE_CHECKING
import json

# Import for type hints only
if TYPE_CHECKING:
    from .VapixAPI import VapixAPI


class DoorControl:

    def __init__(self, api: VapixAPI) -> None:
        
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

    def _check_action(self, token, action) -> dict:
        """
        Gets the door info.

        Returns:
            list: A dictionary containing door state info.
        """
        state = self.get_state(token=token)
        info = self.get_info(token=token)

        if action in self.actions_table[state['DoorMode']] and info[0]["Capabilities"][action]:
            return True
        else:
            return False

class Door(DoorControl):

    def __init__(self, api: VapixAPI, token) -> None:
        self.api = api
        self.api.base_url = "http://" + self.api.host + "/vapix"

        self.token = token

        self.DoorPhysicalState = 'Closed'
        self.Alarm = 'Normal'
        self.Mode = 'Unlocked'
        self.LastUpdate = True
        self.Status = 'State Updated'
        self.info = {}
    
    def update_info(self) -> dict:
        """
        Gets the door info.

        Returns:
            list: A dictionary containing door info.
        """
        resp = self.api._send_request(
            "doorcontrol/GetDoorInfo",
            params={"Token": self.token},
        )

        data = json.loads(resp)

        self.info = data

    def update_state(self) -> dict:
        """
        Gets the door info.

        Returns:
            list: A dictionary containing door state info.
        """
        resp = self.api._send_request(
            "doorcontrol/GetDoorState",
            params={"Token": self.token},
        )

        data = json.loads(resp)

        self.DoorPhysicalState = data.DoorPhysicalState
        self.Alarm = data.Alarm
        self.Mode = data.DoorMode

    def _update_mode(self, action) -> dict:
        """
        Update Door.
        """

        if action in actions and self._check_action(token=self.token, action=action):

            state = self.update_state(self)

            resp = self.api._send_request(
                ("doorcontrol/" + action + "Door"),
                params={"Token": self.token},
            )

            state = self.update_state(self)

            if state['DoorMode'].startswith(action):
                self.LastUpdate = True
                self.Status = "State Updated"
            else:
                self.LastUpdate = False
                self.Status = "State Not Updated"

        else:
            state = self.get_state(token=token)

            self.LastUpdate = False
            self.Status = "Action Not Supported"

from .api import api
from .DoorControl import DoorControl
from .Schedule import ScheduleEndpoint

class a1001:
    """
    A class that provides an interface to interact with Axis A1001
    """

    def __init__(self, host, user, password, timeout=5, removal_limit=30):
        """
        Initializes the Axis A1001
        """
        self.api = api(host=host, user=user, password=password, timeout=timeout)

        self.removal_limit = removal_limit

        self.doorcontrol = DoorControl(self)
        self.schedule = ScheduleEndpoint(api=self.api,removal_limit=self.removal_limit)

from nd_python.endpoints.base.endpoint import SWITCHES


class EpSwitchesInventoryGet:
    """Endpoint to get switch inventory"""

    def __init__(self) -> None:
        self.verb = "GET"
        self.path = SWITCHES
        self.description = "Get Switches Inventory"
        self._fabric_name = ""

    def commit(self) -> None:
        """Commit the endpoint path fabricName query parameter"""
        if not self._fabric_name:
            raise ValueError("fabric_name must be set before committing the endpoint")
        self.path = f"{SWITCHES}?fabricName={self._fabric_name}"

    @property
    def fabric_name(self) -> str:
        """Set (setter) or return (getter) the fabric name"""
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value: str) -> None:
        self._fabric_name = value

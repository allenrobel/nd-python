from nd_python.validators.endpoints.manage import EpCredentialsDefaultSwitchSaveValidator, EpCredentialsRobotSwitchSaveValidator
from pydantic import ValidationError

base = "/api/v1/manage"
credentials = f"{base}/credentials"


class EpCredentialsDefaultSwitchDelete:
    """Endpoint to delete default switch credentials"""

    def __init__(self) -> None:
        self.verb = "DELETE"
        self.path = f"{credentials}/defaultSwitchCredentials"
        self.description = "Delete Default Switch Credentials"


class EpCredentialsDetailsGet:
    """Endpoint to get credentials details"""

    def __init__(self) -> None:
        self.verb = "GET"
        self.path = f"{credentials}/details"
        self.description = "Get Credentials Details"


class EpCredentialsDefaultSwitchGet:
    """Endpoint to get default switch credentials"""

    def __init__(self) -> None:
        self.verb = "GET"
        self.path = f"{credentials}/defaultSwitchCredentials"
        self.description = "Get Default Switch Credentials"


class EpCredentialsDefaultSwitchSave:
    """
    # Summary

    Endpoint to save default switch credentials

    ## Usage

    ```python
    ep = EpCredentialsDefaultSwitchSave()
    ep.switch_username = "admin"
    ep.switch_password = "password"
    ep.commit()
    response = client.request(ep.verb, ep.path, json=ep.body)
    ```
    """

    def __init__(self) -> None:
        self._committed = False
        self.validator = EpCredentialsDefaultSwitchSaveValidator
        self._body: dict = {}
        self.verb = "POST"
        self.path = f"{credentials}/defaultSwitchCredentials"
        self.description = "Save Default Switch Credentials"

    def commit(self) -> None:
        """commit the endpoint"""
        try:
            self.validator(**self._body)
        except ValidationError as error:
            raise ValueError(f"Invalid request body: {error}") from error
        self._committed = True

    @property
    def body(self) -> dict:
        """return a dictionary representing the endpoint payload"""
        if not self._committed:
            raise ValueError("Call instance.commit() before accessing instance.body.")
        return self._body

    @property
    def switch_password(self) -> str:
        """Set (setter) or return (getter) the switch password"""
        return self._body.get("switchPassword", "")

    @switch_password.setter
    def switch_password(self, value: str) -> None:
        self._body["switchPassword"] = value

    @property
    def switch_username(self) -> str:
        """Set (setter) or return (getter) the switch username"""
        return self._body.get("switchUsername", "")

    @switch_username.setter
    def switch_username(self, value: str) -> None:
        self._body["switchUsername"] = value


class EpCredentialsRobotSwitchDelete:
    """Endpoint to delete robot switch credentials"""

    def __init__(self) -> None:
        self.verb = "DELETE"
        self.path = f"{credentials}/robotSwitchCredentials"
        self.description = "Delete Robot Switch Credentials"


class EpCredentialsRobotSwitchGet:
    """Endpoint to get robot switch credentials"""

    def __init__(self) -> None:
        self.verb = "GET"
        self.path = f"{credentials}/robotSwitchCredentials"
        self.description = "Get Robot Switch Credentials"


class EpCredentialsRobotSwitchSave:
    """
    # Summary

    Endpoint to save robot switch credentials

    ## Usage

    ```python
    ep = EpCredentialsRobotSwitchSave()
    ep.switch_username = "admin"
    ep.switch_password = "password"
    ep.commit()
    response = client.request(ep.verb, ep.path, json=ep.body)
    ```
    """

    def __init__(self) -> None:
        self._committed = False
        self.validator = EpCredentialsRobotSwitchSaveValidator
        self._body: dict = {}
        self.verb = "POST"
        self.path = f"{credentials}/robotSwitchCredentials"
        self.description = "Save Robot Switch Credentials"

    def commit(self) -> None:
        """commit the endpoint"""
        try:
            self.validator(**self._body)
        except ValidationError as error:
            raise ValueError(f"Invalid request body: {error}") from error
        self._committed = True

    @property
    def body(self) -> dict:
        """return a dictionary representing the endpoint payload"""
        if not self._committed:
            raise ValueError("Call instance.commit() before accessing instance.body.")
        self._body["isRobot"] = True
        return self._body

    @property
    def switch_password(self) -> str:
        """Set (setter) or return (getter) the switch password"""
        return self._body.get("switchPassword", "")

    @switch_password.setter
    def switch_password(self, value: str) -> None:
        self._body["switchPassword"] = value

    @property
    def switch_username(self) -> str:
        """Set (setter) or return (getter) the switch username"""
        return self._body.get("switchUsername", "")

    @switch_username.setter
    def switch_username(self, value: str) -> None:
        self._body["switchUsername"] = value

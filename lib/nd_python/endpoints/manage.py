from nd_python.validators.endpoints.manage import EpSaveDefaultSwitchCredentials
from pydantic import ValidationError

base = "/api/v1/manage"
credentials = f"{base}/credentials"


class DeleteDefaultSwitchCredentials:
    """Endpoint to delete default switch credentials"""

    def __init__(self):
        self.verb = "DELETE"
        self.path = f"{credentials}/defaultSwitchCredentials"
        self.description = "Delete Default Switch Credentials"


class GetCredentialsDetails:
    """Endpoint to get credentials details"""

    def __init__(self):
        self.verb = "GET"
        self.path = f"{credentials}/details"
        self.description = "Get Credentials Details"


class GetDefaultSwitchCredentials:
    """Endpoint to get default switch credentials"""

    def __init__(self):
        self.verb = "GET"
        self.path = f"{credentials}/defaultSwitchCredentials"
        self.description = "Get Default Switch Credentials"


class SaveDefaultSwitchCredentials:
    """
    # Summary

    Endpoint to save default switch credentials

    ## Usage

    ```python
    ep = SaveDefaultSwitchCredentials()
    ep.switch_username = "admin"
    ep.switch_password = "password"
    ep.commit()
    response = client.request(ep.verb, ep.path, json=ep.body)
    ```
    """

    def __init__(self):
        self._committed = False
        self.validator = EpSaveDefaultSwitchCredentials
        self._body = {}
        self.verb = "POST"
        self.path = f"{credentials}/defaultSwitchCredentials"
        self.description = "Save Default Switch Credentials"

    def commit(self):
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
    def switch_password(self):
        """Set (setter) or return (getter) the switch password"""
        return self._body.get("switchPassword")

    @switch_password.setter
    def switch_password(self, value):
        self._body["switchPassword"] = value

    @property
    def switch_username(self):
        """Set (setter) or return (getter) the switch username"""
        return self._body.get("switchUsername")

    @switch_username.setter
    def switch_username(self, value):
        self._body["switchUsername"] = value

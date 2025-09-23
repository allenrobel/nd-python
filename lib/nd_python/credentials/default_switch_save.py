"""
# Name

default_switch_save.py

# Description

Save default switch credentials to the controller.

# Payload Example

```json
{
    "switchUsername": "admin",
    "switchPassword": "password"
}
```
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging

from nd_python.common.properties import Properties
from nd_python.endpoints.manage import EpSaveDefaultSwitchCredentials


class CredentialsDefaultSwitchSave:
    """
    # Summary

    Save default switch credentials to the controller.

    ## Example default switch save request

    ### See

    ./examples/credentials_default_switch_save.py
    """

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__
        self.endpoint = EpSaveDefaultSwitchCredentials()
        self.log = logging.getLogger(f"nd_python.{self.class_name}")
        self.properties = Properties()
        self.rest_send = self.properties.rest_send

        self._payload: dict[str, str] = {}
        self._switch_username = ""
        self._switch_password = ""

    def _final_verification(self) -> None:
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]

        if self.rest_send is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.rest_send must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self._switch_username == "":
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Call {self.class_name}.switch_username "
            msg += f"before calling {self.class_name}.commit"
            raise ValueError(msg)
        if self._switch_password == "":
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Call {self.class_name}.switch_password "
            msg += f"before calling {self.class_name}.commit"
            raise ValueError(msg)

    def commit(self) -> None:
        """
        Create a network
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        self.endpoint.switch_username = self._switch_username
        self.endpoint.switch_password = self._switch_password
        try:
            self.endpoint.commit()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Unable to validate endpoint. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        self._payload["switchUsername"] = self.endpoint.switch_username
        self._payload["switchPassword"] = self.endpoint.switch_password
        try:
            self.rest_send.path = self.endpoint.path
            self.rest_send.verb = self.endpoint.verb
            self.rest_send.payload = self._payload
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

    @property
    def switch_password(self) -> str:
        """
        Set (setter) or return (getter) the current value of switch_password
        """
        return self._switch_password

    @switch_password.setter
    def switch_password(self, value):
        self._switch_password = value

    @property
    def switch_username(self) -> str:
        """
        Set (setter) or return (getter) the current value of switch_username
        """
        return self._switch_username

    @switch_username.setter
    def switch_username(self, value):
        self._switch_username = value

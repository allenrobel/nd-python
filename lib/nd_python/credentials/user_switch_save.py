"""
# Name

robot_switch_get.py

# Description

Save user switch credentials to the controller.

# Payload Example

```json
{
  "switchIds": [
    {
      "switchId": "SAL1948TRTT"
    },
    {
      "switchId": "SAL1947TRAB"
    }
  ],
  "switchPassword": "test",
  "switchUsername": "admin"
}
```
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging
from typing import Any

from nd_python.common.properties import Properties
from nd_python.endpoints.manage import EpCredentialsUserSwitchSave
from nd_python.switches.inventory_get import SwitchesInventoryGet


class CredentialsUserSwitchSave:
    """
    # Summary

    Save user switch credentials to the controller.

    ## Example user switch save request

    ### See

    ./examples/credentials_user_switch_save.py
    """

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__
        self.endpoint = EpCredentialsUserSwitchSave()
        self.inventory = SwitchesInventoryGet()
        self.log = logging.getLogger(f"nd_python.{self.class_name}")
        self.properties = Properties()
        self.rest_send = self.properties.rest_send

        self._committed = False
        self._fabric_name = ""
        self._payload: dict[str, Any] = {}
        self._switch_name = ""
        self._switch_username = ""
        self._switch_password = ""

    def _verify_property(self, method_name: str, property_name: str) -> None:
        if not getattr(self, property_name, None):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.{property_name} must be set before callling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

    def _final_verification(self) -> None:
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        self._verify_property(method_name, "fabric_name")
        self._verify_property(method_name, "rest_send")
        self._verify_property(method_name, "switch_name")
        self._verify_property(method_name, "switch_password")
        self._verify_property(method_name, "switch_username")

    def build_payload(self) -> None:
        """
        Build the payload for the request
        """
        self._payload = {}
        self.inventory.fabric_name = self.fabric_name
        self.inventory.rest_send = self.rest_send
        self.inventory.commit()
        serial_number = self.inventory.switch_name_to_serial_number(self.switch_name)
        if not serial_number:
            msg = f"switch_name {self.switch_name} not found in fabric {self.fabric_name}"
            raise ValueError(msg)

        self._payload = {
            "switchIds": [{"switchId": serial_number}],
            "switchUsername": self.switch_username,
            "switchPassword": self.switch_password,
        }

    def commit(self) -> None:
        """
        Save user switch credentials to the controller
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()
        self.build_payload()

        try:
            self.rest_send.path = self.endpoint.path
            self.rest_send.verb = self.endpoint.verb
            self.rest_send.payload = self._payload
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error sending {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        self._committed = True

    @property
    def fabric_name(self) -> str:
        """
        Set (setter) or return (getter) fabric_name
        """
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value: str) -> None:
        self._fabric_name = value

    @property
    def switch_name(self) -> str:
        """
        Set (setter) or return (getter) switch_name
        """
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value: str) -> None:
        self._switch_name = value

    @property
    def switch_password(self) -> str:
        """
        Set (setter) or return (getter) switch_password
        """
        return self._switch_password

    @switch_password.setter
    def switch_password(self, value: str) -> None:
        self._switch_password = value

    @property
    def switch_username(self) -> str:
        """
        Set (setter) or return (getter) switch_username
        """
        return self._switch_username

    @switch_username.setter
    def switch_username(self, value: str) -> None:
        self._switch_username = value

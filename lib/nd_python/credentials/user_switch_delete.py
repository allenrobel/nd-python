"""
# Name

user_switch_delete.py

# Description

Delete user switch credentials from the controller.

# Payload Example

```json
{
  "switchIds": [
    "SAL1948TRTT",
    "SAL1947TRAB"
  ]
}
```
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging

from nd_python.common.properties import Properties
from nd_python.endpoints.manage import EpCredentialsUserSwitchDelete
from nd_python.switches.inventory_get import SwitchesInventoryGet
from nd_python.validators.credentials.user_switch_delete import CredentialsUserSwitchDeleteConfigValidator


class CredentialsUserSwitchDelete:
    """
    # Summary

    Delete user switch credentials from the controller.

    ## Example user switch delete request

    ### See

    ./examples/credentials_user_switch_delete.py
    """

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__
        self.endpoint = EpCredentialsUserSwitchDelete()
        self.inventory = SwitchesInventoryGet()
        self.log = logging.getLogger(f"nd_python.{self.class_name}")
        self.properties = Properties()
        self.rest_send = self.properties.rest_send

        self._committed = False
        self._config: dict[str, list[dict]] = {}
        self._fabric_name = ""
        self._fabric_inventory: dict[str, dict] = {}
        self._payload: dict[str, list[str]] = {}
        self._result: str = ""
        self._switch_name = ""

    def _verify_property(self, method_name: str, property_name: str) -> None:
        if not getattr(self, property_name, None):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.{property_name} must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

    def _final_verification(self) -> None:
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        self._verify_property(method_name, "config")
        self._verify_property(method_name, "rest_send")

    def populate_fabric_inventory(self, fabric_name: str) -> None:
        """
        Add fabric_name, if it exists, to self._fabric_inventory
        """
        method_name = inspect.stack()[0][3]
        if fabric_name in self._fabric_inventory:
            return
        self.inventory.fabric_name = fabric_name
        self.inventory.rest_send = self.rest_send
        try:
            self.inventory.commit()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error populating fabric inventory for fabric {fabric_name}. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        self._fabric_inventory[fabric_name] = self.inventory.inventory_by_switch_name

    def build_payload(self) -> None:
        """
        Build the payload for the request
        """
        self._payload = {}
        _serial_numbers = []
        for item in self.config:
            self.populate_fabric_inventory(item.fabric_name)
            serial_number = self._fabric_inventory.get(item.fabric_name, {}).get(item.switch_name, {}).get("serialNumber", "")
            if not serial_number:
                msg = f"switch_name {item.switch_name} not found in fabric {item.fabric_name}"
                raise ValueError(msg)
            self.result = f"Fabric {item.fabric_name} switch {item.switch_name} serial number {serial_number}.\n"
            _serial_numbers.append(serial_number)
        if len(_serial_numbers) == 0:
            msg = "No valid switches found to delete credentials"
            raise ValueError(msg)
        self._payload = {
            "switchIds": _serial_numbers,
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
    def config(self) -> CredentialsUserSwitchDeleteConfigValidator:
        """
        Set (setter) or return (getter) the configuration as a Pydantic model
        """
        return self._config

    @config.setter
    def config(self, value: CredentialsUserSwitchDeleteConfigValidator) -> None:
        self._config = value

    @property
    def fabric_inventory(self) -> dict[str, dict]:
        """
        Return fabric_inventory (dict[str, dict])

        Keyed on fabric_name, value is a dict keyed on switch_name with
        values of dicts containing switch details.
        """
        method_name = inspect.stack()[0][3]
        if not self._committed:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.commit must be called before accessing "
            msg += f"{self.class_name}.{method_name}"
            raise ValueError(msg)
        return self._fabric_inventory

    @property
    def result(self) -> str:
        """
        Result of the commit operation.

        Set (setter) or return (getter) the result as a string

        The setter appends to the result string.
        """
        method_name = inspect.stack()[0][3]
        if not self._committed:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.commit must be called before accessing "
            msg += f"{self.class_name}.{method_name}"
            raise ValueError(msg)
        return self._result

    @result.setter
    def result(self, value: str) -> None:
        self._result += value

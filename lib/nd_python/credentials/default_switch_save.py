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
from nd_python.endpoints.manage import EpCredentialsDefaultSwitchSave
from nd_python.validators.credentials.default_switch_save import CredentialsDefaultSwitchSaveConfigValidator


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
        self.endpoint = EpCredentialsDefaultSwitchSave()
        self.log = logging.getLogger(f"nd_python.{self.class_name}")
        self.properties = Properties()
        self.rest_send = self.properties.rest_send

        self._config = None
        self._payload: dict[str, str] = {}

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

    def commit(self) -> None:
        """
        Create a network
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        self.endpoint.switch_username = self._config.switch_username
        self.endpoint.switch_password = self._config.switch_password
        try:
            self.endpoint.commit()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Unable to validate endpoint. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        self._payload["switchUsername"] = self._config.switch_username
        self._payload["switchPassword"] = self._config.switch_password
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
    def config(self) -> CredentialsDefaultSwitchSaveConfigValidator:
        """
        Set (setter) or return (getter) the current value of config
        """
        return self._config

    @config.setter
    def config(self, value: CredentialsDefaultSwitchSaveConfigValidator) -> None:
        self._config = value

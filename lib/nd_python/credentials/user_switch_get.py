"""
# Name

user_switch_get.py

# Description

Retrieve user switch credentials from the controller.

# Payload Example

This endpoint does not require a payload.
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging

from nd_python.common.properties import Properties
from nd_python.endpoints.manage import EpCredentialsUserSwitchGet


class CredentialsUserSwitchGet:
    """
    # Summary

    Get user switch credentials from the controller.

    ## Example user switch get request

    ``` python
    instance = CredentialsUserSwitchGet()
    instance.rest_send = rest_send
    instance.commit()
    instance.filter = "mySwitchName"
    instance.set_filtered_data()
    print(f"data: {json.dumps(instance.data, indent=4, sort_keys=True)}")
    print(f"filtered_data: {json.dumps(instance.filtered_data, indent=4, sort_keys=True)}")
    print(f"credential_store: {instance.credential_store}")
    print(f"switch_name: {instance.switch_name}")
    print(f"switch_username: {instance.switch_username}")
    ```

    ### See example script

    ./examples/credentials_user_switch_get.py
    """

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__
        self.endpoint = EpCredentialsUserSwitchGet()
        self.log = logging.getLogger(f"nd_python.{self.class_name}")
        self.properties = Properties()
        self.rest_send = self.properties.rest_send
        self._committed = False
        self.data_filtered = False
        self._filter = ""
        self._filtered_data = {"credentialStore": "", "fabricName": "", "ip": "", "switchId": "", "switchName": "", "switchUsername": "", "type": ""}

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

    def commit(self) -> None:
        """
        Retrieve user switch credentials from the controller
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        try:
            self.rest_send.path = self.endpoint.path
            self.rest_send.verb = self.endpoint.verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to get {self.rest_send.verb} request from the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        self._committed = True

    def set_filtered_data(self) -> None:
        """
        Set the filtered data from the response
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)

        if not self._filter:
            return

        self.data_filtered = True

        if not self.data:
            return

        for item in self.data:
            if not isinstance(item, dict):
                continue
            if not item.get("switchName", "") == self._filter:
                continue
            self._filtered_data = item

    def error_if_not_committed(self, method_name) -> None:
        """
        Raise an error if .commit() has not been called
        """
        if not self._committed:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.commit() must be called before accessing {method_name}"
            raise ValueError(msg)

    @property
    def credential_store(self) -> str:
        """
        Return credentialStore from the filtered data
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)
        return self._filtered_data.get("credentialStore", "")

    @property
    def credential_type(self) -> str:
        """
        Return type from the filtered data
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)
        return self._filtered_data.get("type", "")

    @property
    def data(self) -> list:
        """
        Return the data from the response
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)
        return self.rest_send.response_current.get("DATA", {}).get("items", [])

    @property
    def fabric_name(self) -> str:
        """
        Return fabricName from the filtered data
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)
        return self._filtered_data.get("fabricName", "")

    @property
    def filter(self) -> str:
        """
        Return user filter
        """
        return self._filter

    @filter.setter
    def filter(self, value: str) -> None:
        """
        Set user filter.

        filter is a string representing the switch name.
        """
        method_name = inspect.stack()[0][3]
        if not isinstance(value, str):
            msg = f"{self.class_name}.{method_name}: "
            msg += "filter must be a string. "
            msg += f"Got: {type(value)} ({value})"
            raise ValueError(msg)
        self._filter = value

    @property
    def filtered_data(self) -> dict:
        """
        Return filtered data
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)
        return self._filtered_data

    @property
    def ip(self) -> str:
        """
        Return ip from the filtered data
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)
        return self._filtered_data.get("ip", "")

    @property
    def switch_id(self) -> str:
        """
        Return switchId from the filtered data
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)
        return self._filtered_data.get("switchId", "")

    @property
    def switch_name(self) -> str:
        """
        Return switchName from the filtered data
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)
        return self._filtered_data.get("switchName", "")

    @property
    def switch_username(self) -> str:
        """
        Return switchUsername from the filtered data
        """
        method_name = inspect.stack()[0][3]
        self.error_if_not_committed(method_name)
        return self._filtered_data.get("switchUsername", "")

"""
# Name

inventory_get.py

# Description

Retrieve switch inventory for a fabric.

# Payload Example

This endpoint does not require a payload.
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging
from copy import deepcopy

from nd_python.common.properties import Properties
from nd_python.endpoints.switches.inventory_get import EpSwitchesInventoryGet


class SwitchesInventoryGet:
    """
    # Summary

    Get switches inventory for a fabric from the controller.

    ## Example switches inventory get request

    ### See

    ./examples/switches_inventory_get.py
    """

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__
        self.endpoint = EpSwitchesInventoryGet()
        self.log = logging.getLogger(f"nd_python.{self.class_name}")
        self.properties = Properties()
        self.rest_send = self.properties.rest_send
        self._committed: bool = False
        self._fabric_name: str = ""
        self._inventory_by_switch_name: dict = {}
        self._inventory_by_switch_ipv4_address: dict = {}
        self._inventory_by_switch_serial_number: dict = {}
        self._inventory_data: list = []
        self._inventory_meta: dict = {}
        self._request_path: str = ""
        self._request_method: str = ""
        self._response_message: str = ""
        self._return_code: int = 0

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

        if not self.fabric_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.fabric_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

    def commit(self) -> None:
        """
        Retrieve switch inventory for a fabric from the controller
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        self.endpoint.fabric_name = self.fabric_name
        self.endpoint.commit()

        try:
            self.rest_send.path = self.endpoint.path
            self.rest_send.verb = self.endpoint.verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error sending {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        self._inventory_data = self.rest_send.response_current.get("DATA", {}).get("switches", [])
        self._inventory_meta = self.rest_send.response_current.get("DATA", {}).get("meta", {})
        self._request_method = self.rest_send.response_current.get("REQUEST_METHOD", "")
        self._request_path = self.rest_send.response_current.get("REQUEST_PATH", "")
        self._response_message = self.rest_send.response_current.get("MESSAGE", "")
        self._return_code = int(self.rest_send.response_current.get("RETURN_CODE", 0))

        self._build_inventory_by_switch_ipv4_address()
        self._build_inventory_by_switch_name()
        self._build_inventory_by_switch_serial_number()
        self._committed = True

    def _build_inventory_by_switch_ipv4_address(self) -> None:
        """Build the fabric inventory keyed on switch IPv4 address."""
        self._inventory_by_switch_ipv4_address = {}
        for switch in self._inventory_data:
            key = switch.get("fabricManagementIp")
            if key is None:
                continue
            self._inventory_by_switch_ipv4_address[key] = deepcopy(switch)

    def _build_inventory_by_switch_name(self) -> None:
        """Build the fabric inventory keyed on switch name."""
        self._inventory_by_switch_name = {}
        for switch in self._inventory_data:
            key = switch.get("hostname")
            if key is None:
                continue
            self._inventory_by_switch_name[key] = deepcopy(switch)

    def _build_inventory_by_switch_serial_number(self) -> None:
        """Build the fabric inventory keyed on switch serial number."""
        self._inventory_by_switch_serial_number = {}
        for switch in self._inventory_data:
            key = switch.get("serialNumber")
            if key is None:
                continue
            self._inventory_by_switch_serial_number[key] = deepcopy(switch)

    def is_vpc_peer(self, switch_name: str, peer_switch_name: str) -> bool:
        """
        # Summary

        Determine if two switches are vPC peers.

        - Return True if switch_name and peer_switch_name are vPC peers.
        - Return False otherwise.

        ## Raises

        - ValueError if either switch_name or peer_switch_name are not found in the fabric inventory.

        ## TODO

        - The 4.1 API endpoint response does not contain peer serial number for VPC peers.
        - We need another way to determine if two switches are VPC peers.
        - For now, we will assume that if both switches are VPC configured, they are peers.
        - Update 2025-09-24: It may be that vpcData is not populated unless vpcConfigure is True.
        - Need to test this and update the code accordingly.

        """
        if not self._committed:
            self.commit()

        serial_number = self.switch_name_to_serial_number(switch_name)
        peer_serial_number = self.switch_name_to_serial_number(peer_switch_name)

        # The above will raise if either switch_name or peer_switch_name are not found.
        # If we reach here, both switches exist in the fabric inventory.
        switch = self._inventory_by_switch_name.get(switch_name, {})
        peer_switch = self._inventory_by_switch_name.get(peer_switch_name, {})

        if switch.get("vpcConfigured", False) is not True:
            return False
        if peer_switch.get("vpcConfigured", False) is not True:
            return False
        if serial_number == peer_serial_number:
            return False

        return True

    def switch_name_to_serial_number(self, switch_name: str) -> str:
        """
        # Summary

        Given a switch_name, return the associated serial number.

        ## Raises

        - ValueError if switch_name is not found in the fabric inventory.
        - ValueError if the switch does not have a serial number.
        """
        if not self._committed:
            self.commit()
        switch = self._inventory_by_switch_name.get(switch_name)
        if switch is None:
            msg = f"Switch name {switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        serial_number = switch.get("serialNumber")
        if serial_number is None:
            msg = f"Switch name {switch_name} has no serial number in fabric {self.fabric_name}."
            raise ValueError(msg)
        return serial_number

    def switch_name_to_ipv4_address(self, switch_name: str) -> str:
        """
        Given a switch_name, return the associated IPv4 address.
        """
        if not self._committed:
            self.commit()
        switch = self._inventory_by_switch_name.get(switch_name)
        if switch is None:
            msg = f"Switch name {switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        ipv4_address = switch.get("fabricManagementIp")
        if ipv4_address is None:
            msg = f"Switch name {switch_name} has no IPv4 address in fabric {self.fabric_name}."
            raise ValueError(msg)
        return ipv4_address

    def ipv4_address_to_switch_name(self, ipv4_address: str) -> str:
        """
        Given an IPv4 address, return the associated switch name.
        """
        if not self._committed:
            self.commit()
        switch = self._inventory_by_switch_ipv4_address.get(ipv4_address)
        if switch is None:
            msg = f"IPv4 address {ipv4_address} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        switch_name = switch.get("hostname")
        if switch_name is None:
            msg = f"IPv4 address {ipv4_address} has no associated switch name in fabric {self.fabric_name}."
            raise ValueError(msg)
        return switch_name

    def ipv4_address_to_serial_number(self, ipv4_address: str) -> str:
        """
        Given an IPv4 address, return the associated serial number.
        """
        if not self._committed:
            self.commit()
        switch = self._inventory_by_switch_ipv4_address.get(ipv4_address)
        if switch is None:
            msg = f"IPv4 address {ipv4_address} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        serial_number = switch.get("serialNumber")
        if serial_number is None:
            msg = f"IPv4 address {ipv4_address} has no associated serial number in fabric {self.fabric_name}."
            raise ValueError(msg)
        return serial_number

    def serial_number_to_ipv4_address(self, serial_number: str) -> str:
        """
        Given a serial number, return the associated IPv4 address.
        """
        if not self._committed:
            self.commit()
        switch = self._inventory_by_switch_serial_number.get(serial_number)
        if switch is None:
            msg = f"Serial number {serial_number} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        ipv4_address = switch.get("fabricManagementIp")
        if ipv4_address is None:
            msg = f"Serial number {serial_number} has no associated IPv4 address in fabric {self.fabric_name}."
            raise ValueError(msg)
        return ipv4_address

    def serial_number_to_switch_name(self, serial_number: str) -> str:
        """
        Given a serial number, return the associated switch name.
        """
        if not self._committed:
            self.commit()
        switch = self._inventory_by_switch_serial_number.get(serial_number)
        if switch is None:
            msg = f"Serial number {serial_number} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        switch_name = switch.get("hostname")
        if switch_name is None:
            msg = f"Serial number {serial_number} has no associated switch name in fabric {self.fabric_name}."
            raise ValueError(msg)
        return switch_name

    @property
    def data(self) -> dict:
        """
        Get the data from the response
        """
        if not self._committed:
            self.commit()
        return self.rest_send.response_current.get("DATA", {})

    @property
    def devices(self) -> list:
        """
        return a list of device names in the fabric inventory
        """
        if not self._committed:
            self.commit()
        return list(self._inventory_by_switch_name.keys())

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
    def inventory_by_switch_ipv4_address(self) -> dict:
        """
        return the fabric inventory dictionary keyed on fabricManagementIp
        """
        if not self._committed:
            self.commit()
        return self._inventory_by_switch_ipv4_address

    @property
    def inventory_by_switch_name(self) -> dict:
        """
        return the fabric inventory dictionary keyed on switch name
        """
        if not self._committed:
            self.commit()
        return self._inventory_by_switch_name

    @property
    def inventory_by_switch_serial_number(self) -> dict:
        """
        return the fabric inventory dictionary keyed on switch serial number
        """
        if not self._committed:
            self.commit()
        return self._inventory_by_switch_serial_number

    @property
    def inventory_meta(self) -> dict:
        """
        return the fabric inventory metadata
        """
        if not self._committed:
            self.commit()
        return self._inventory_meta

    @property
    def request_method(self) -> str:
        """
        return the current value of METHOD from the response as a string
        """
        if not self._committed:
            self.commit()
        return self._request_method

    @property
    def request_path(self) -> str:
        """
        return the current value of REQUEST_PATH from the response as a string
        """
        if not self._committed:
            self.commit()
        return self._request_path

    @property
    def response_message(self) -> str:
        """
        return the current value of MESSAGE from the response as a string
        """
        if not self._committed:
            self.commit()
        return self._response_message

    @property
    def return_code(self) -> int:
        """
        return the current value of return_code as an integer
        """
        if not self._committed:
            self.commit()
        return self._return_code

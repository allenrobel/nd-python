"""
# Name

credentials_details_get.py

# Description

Retrieve credentials details from the controller.

# Payload Example

This endpoint does not require a payload.
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging

from nd_python.common.properties import Properties
from nd_python.endpoints.manage import EpCredentialsDetailsGet


class CredentialsDetailsGet:
    """
    # Summary

    Get credentials details from the controller.

    ## Example get request

    ### See

    ./examples/credentials_details_get.py
    """

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__
        self.endpoint = EpCredentialsDetailsGet()
        self.log = logging.getLogger(f"nd_python.{self.class_name}")
        self.properties = Properties()
        self.rest_send = self.properties.rest_send
        self._committed = False

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
        Retrieve credentials details from the controller
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        try:
            self.rest_send.path = self.endpoint.path
            self.rest_send.verb = self.endpoint.verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        self._committed = True

    @property
    def data(self) -> dict:
        """
        Get the data from the response
        """
        method_name = inspect.stack()[0][3]
        if not self._committed:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.commit() must be called before accessing data"
            raise ValueError(msg)
        return self.rest_send.response_current.get("DATA", {})

#
# Copyright (c) 2025 Cisco and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

__metaclass__ = type
__author__ = "Allen Robel"

import enum
import inspect
import logging

from nd_python.common.response_generator_protocol import ResponseGeneratorProtocol


@enum.unique
class Exceptions(enum.Enum):
    """Supported exceptions for simulation."""

    VALUE_ERROR = ValueError
    TYPE_ERROR = TypeError
    KEY_ERROR = KeyError
    INDEX_ERROR = IndexError
    ATTRIBUTE_ERROR = AttributeError
    NOT_IMPLEMENTED_ERROR = NotImplementedError
    RUNTIME_ERROR = RuntimeError
    EXCEPTION = Exception


class Sender:
    """
    ### Summary
    An injected dependency for ``RestSend`` which implements the
    ``sender`` interface.  Responses are read from JSON files.

    ### Raises
    -   ``ValueError`` if:
            -   ``gen`` is not set.
    -   ``TypeError`` if:
            -   ``gen`` is not an instance of ResponseGenerator()

    ### Usage
    ``responses()`` is a coroutine that yields controller responses.
    In the example below, it yields to dictionaries.  However, in
    practice, it would yield responses read from JSON files.

    ```python
    def responses():
        yield {"key1": "value1"}
        yield {"key2": "value2"}

    sender = Sender()
    sender.gen = ResponseGenerator(responses())

    try:
        rest_send = RestSend()
        rest_send.sender = sender
    except (TypeError, ValueError) as error:
        handle_error(error)
    # etc...
    # See rest_send_v2.py for RestSend() usage.
    ```
    """

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__

        self.log = logging.getLogger(f"nd_python.{self.class_name}")

        self._ansible_module = None
        self._gen: ResponseGeneratorProtocol | None = None
        self._implements = "sender_v1"
        self._path: str = ""
        self._payload = None
        self._response = None
        self._verb: str = ""

        self._raise_method: str = "unknown"
        self._raise_message: str = "Simulated exception for testing"
        self._raise_exception: Exceptions | None = None

        msg = "ENTERED Sender(): "
        self.log.debug(msg)

    def _verify_commit_parameters(self) -> None:
        """
        ### Summary
        Verify that required parameters are set prior to calling ``commit()``

        ### Raises
        -   ``ValueError`` if ``verb`` is not set
        -   ``ValueError`` if ``path`` is not set
        """
        method_name = inspect.stack()[0][3]
        if self.gen is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "gen must be set before calling commit()."
            raise ValueError(msg)

    def _check_and_raise(self, method_name: str) -> None:
        """
        Check if this method should raise an exception.
        Call this at the start of each method that supports simulation.
        """
        if self._raise_method == method_name and self._raise_exception is not None:
            raise self._raise_exception.value(self._raise_message)

    def commit(self) -> None:
        """
        ### Summary
        Dummy commit

        ### Raises
        -   ``ValueError`` if ``gen`` is not set.
        -   ``self.raise_exception`` if set and
            ``self.raise_method`` == "commit"
        """
        method_name = inspect.stack()[0][3]
        self._check_and_raise(method_name)

        try:
            self._verify_commit_parameters()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Not all mandatory parameters are set. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        method_name = inspect.stack()[0][3]
        caller = inspect.stack()[1][3]
        msg = f"{self.class_name}.{method_name}: "
        msg += f"caller {caller}"
        self.log.debug(msg)

    @property
    def ansible_module(self) -> None:
        """
        ### Summary
        Dummy ansible_module
        """
        return self._ansible_module

    @ansible_module.setter
    def ansible_module(self, value) -> None:
        self._ansible_module = value

    @property
    def gen(self) -> ResponseGeneratorProtocol:
        """
        ### Summary
        -   getter: Return the ``ResponseGenerator()`` instance.
        -   setter: Set the ``ResponseGenerator()`` instance that provides
            simulated responses.

        ### Raises
        ``TypeError`` if value is not a class implementing the
        ResponseGeneratorProtocol interface.

        ### Notes
        See ``common/response_generator_protocol.py`` for the interface definition.
        """
        return self._gen

    @gen.setter
    def gen(self, value: ResponseGeneratorProtocol) -> None:
        method_name = inspect.stack()[0][3]
        msg = f"{self.class_name}.{method_name}: "
        msg += "Expected a class implementing the "
        msg += "response_generator interface. "
        msg += f"Got {value}."
        try:
            implements = value.implements
        except AttributeError as error:
            raise TypeError(msg) from error
        if implements != "response_generator":
            raise TypeError(msg)
        self._gen = value

    @property
    def implements(self) -> str:
        """
        ### Summary
        The interface implemented by this class.

        ### Raises
        None
        """
        return self._implements

    @property
    def path(self) -> str:
        """
        ### Summary
        Dummy path.

        ### Raises
        None

        ### Example
        ``/appcenter/cisco/ndfc/api/v1/...etc...``
        """
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        self._path = value

    @property
    def payload(self) -> dict | None:
        """
        ### Summary
        Dummy payload.

        ### Raises
        -   ``TypeError`` if value is not a ``dict``.
        """
        return self._payload

    @payload.setter
    def payload(self, value: dict | None) -> None:
        self._payload = value

    @property
    def raise_exception(self) -> Exceptions | None:
        """
        ### Summary
        The simulated exception to raise.

        ### Usage
        ```python
        instance = Sender()
        sender.raise_exception = Exceptions.VALUE_ERROR
        sender.raise_message = "Invalid commit data"
        instance.raise_method = "commit"
        instance.commit() # will raise a simulated ValueError
        ```

        ### NOTES
        -   No error checking is done on the input to this property.
        """
        return self._raise_exception

    @raise_exception.setter
    def raise_exception(self, value: Exceptions) -> None:
        self._raise_exception = value

    @property
    def raise_message(self) -> str:
        """Custom message for the raised exception. See ``raise_exception``."""
        return self._raise_message

    @raise_message.setter
    def raise_message(self, value: str) -> None:
        self._raise_message = value

    @property
    def raise_method(self) -> str | None:
        """The method name where exception should be raised. See ``raise_exception``."""
        return self._raise_method

    @raise_method.setter
    def raise_method(self, value: str) -> None:
        self._raise_method = value

    @property
    def response(self) -> dict:
        """
        ### Summary
        The simulated response from a file.

        ### Raises
        None

        -   getter: Return a copy of ``response``
        -   setter: Set ``response``
        """
        self._verify_commit_parameters()
        return self.gen.next  # pylint: disable=no-member

    @property
    def verb(self) -> str:
        """
        ### Summary
        Dummy Verb.

        ### Raises
        None
        """
        return self._verb

    @verb.setter
    def verb(self, value: str) -> None:
        self._verb = value

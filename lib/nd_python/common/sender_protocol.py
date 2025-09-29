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

from typing import Protocol


class SenderProtocol(Protocol):
    """
    ### Summary
    Protocol defining the Sender interface for RestSend.

    Any class implementing this protocol can be used as a sender
    for RestSend operations. This allows for multiple sender
    implementations (e.g., requests-based, file-based, async, mock).

    ### Required Properties
    - implements: Interface version string (e.g., "sender_v1")
    - path: Endpoint path for the REST request
    - verb: HTTP verb (GET, POST, PUT, DELETE)
    - payload: Optional request payload
    - response: Response dictionary from the controller

    ### Required Methods
    - commit(): Send the request and populate response

    ### Example Implementation Check
    ```python
    from nd_python.common.sender_protocol import SenderProtocol
    from nd_python.common.sender_requests import Sender

    def use_sender(sender: SenderProtocol) -> None:
        sender.path = "/api/v1/manage/credentials"
        sender.verb = "GET"
        sender.commit()
        print(sender.response)

    # Both implementations satisfy the protocol
    use_sender(Sender())
    ```
    """

    @property
    def implements(self) -> str:
        """
        ### Summary
        The interface version implemented by this sender.

        ### Returns
        str: Interface version (e.g., "sender_v1")
        """
        ...

    @property
    def path(self) -> str:
        """
        ### Summary
        Endpoint path for the REST request.

        ### Returns
        str: The endpoint path

        ### Example
        "/api/v1/manage/credentials"
        """
        ...

    @path.setter
    def path(self, value: str) -> None:
        """
        ### Summary
        Set the endpoint path for the REST request.

        ### Args
        value (str): The endpoint path
        """
        ...

    @property
    def verb(self) -> str:
        """
        ### Summary
        HTTP verb for the request.

        ### Returns
        str: HTTP verb (GET, POST, PUT, DELETE, PATCH)
        """
        ...

    @verb.setter
    def verb(self, value: str) -> None:
        """
        ### Summary
        Set the HTTP verb for the request.

        ### Args
        value (str): HTTP verb (GET, POST, PUT, DELETE, PATCH)
        """
        ...

    @property
    def payload(self) -> dict | None:
        """
        ### Summary
        Request payload to send to the controller.

        ### Returns
        dict | None: The request payload, or None if no payload
        """
        ...

    @payload.setter
    def payload(self, value: dict | None) -> None:
        """
        ### Summary
        Set the request payload.

        ### Args
        value (dict | None): The request payload, or None for no payload
        """
        ...

    @property
    def response(self) -> dict:
        """
        ### Summary
        Response from the controller after commit().

        ### Returns
        dict: Response dictionary containing RETURN_CODE, DATA, MESSAGE, etc.
        """
        ...

    def commit(self) -> None:
        """
        ### Summary
        Send the REST request and populate the response property.

        ### Raises
        ValueError: If required parameters are not set or request fails
        """
        ...
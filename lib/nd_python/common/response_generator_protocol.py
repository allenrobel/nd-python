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

# pylint: disable=unnecessary-ellipsis

from typing import Protocol


class ResponseGeneratorProtocol(Protocol):
    """
    ### Summary
    Protocol defining the ResponseGenerator interface for file-based senders.

    Any class implementing this protocol can be used as a response generator
    for Sender implementations that read responses from files or other sources.
    This allows for multiple response generator implementations (e.g., file-based,
    in-memory, queue-based).

    ### Required Properties
    - implements: Interface version string (must be "response_generator")
    - next: The next response dictionary to return

    ### Example Implementation Check
    ```python
    from nd_python.common.response_generator_protocol import ResponseGeneratorProtocol

    def responses():
        yield {"key1": "value1"}
        yield {"key2": "value2"}

    class ResponseGenerator:
        def __init__(self, gen):
            self._gen = gen
            self._implements = "response_generator"

        @property
        def implements(self) -> str:
            return self._implements

        @property
        def next(self) -> dict:
            return next(self._gen)

    # Use with Sender
    sender = Sender()
    sender.gen = ResponseGenerator(responses())
    ```
    """

    @property
    def implements(self) -> str:
        """
        ### Summary
        The interface version implemented by this response generator.

        ### Returns
        str: Interface version (must be "response_generator")
        """
        ...

    @property
    def next(self) -> dict:
        """
        ### Summary
        Return the next response from the generator.

        ### Returns
        dict: The next response dictionary containing controller response data

        ### Notes
        This property is called each time a response is needed. The implementation
        should yield responses sequentially from its data source (file, queue, etc.).
        """
        ...

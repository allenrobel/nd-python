from nd_python.common.rest_send_v2 import RestSend
from nd_python.common.results import Results


class Properties:
    """
    # Summary

    Common properties used in the ndfc-python repository
    """

    def __init__(self) -> None:
        self._rest_send: RestSend = RestSend({})
        self._results: Results = Results()

    @property
    def rest_send(self) -> RestSend:
        """
        rest_send: An instance of RestSend
        """
        return self._rest_send

    @rest_send.setter
    def rest_send(self, value: RestSend) -> None:
        self._rest_send = value

    @property
    def results(self) -> Results:
        """
        results: An instance of Results
        """
        return self._results

    @results.setter
    def results(self, value: Results) -> None:
        self._results = value

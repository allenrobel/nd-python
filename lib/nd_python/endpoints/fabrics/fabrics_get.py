from nd_python.endpoints.base.endpoint import FABRICS
from nd_python.endpoints.base.query_filter_generic import QueryFilterGeneric


class EpFabricsGet:
    """Endpoint to get fabrics"""

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__
        self.description = "Get Fabrics"
        self.query_string = QueryFilterGeneric()

        self._path = FABRICS
        self.verb = "GET"

    def commit(self) -> None:
        """Commit the endpoint path fabricName query parameter"""
        self.query_string.commit()
        if self.query_string.query_string:
            self._path = f"{FABRICS}?{self.query_string.query_string}"

    @property
    def path(self) -> str:
        """Set (setter) or return (getter) the fabric name"""
        return self._path

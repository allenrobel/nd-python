import inspect
from urllib.parse import urlencode


class QueryFilterGeneric:
    """
    # Summary

    Generic query filter parameters

    ## Attributes

    - filter: Lucene style filter string.  E.g. "prop1:value1 AND prop2:value2"
    - max: Maximum number of results to return.
    - offset: Number of records to offset into the result set.
    - sort: Comma separated list of properties to sort by.  Prefix with '-' for descending order. E.g. "prop1,-prop2"

    ## Methods

    - commit(): Commit the query filter parameters
    - query_string: Return the query string

    ## Usage

    ```python
    from nd_python.endpoints.base.query_filter_generic import QueryFilterGeneric

    class MyClass:
        def __init__(self):
            self.filter = QueryFilterGeneric()
            self._endpoint = "some/endpoint"

        def commit(self):
            self.filter.commit()
            # call some API endpoint with self.filter.query_string
            path = f"{self._endpoint}?{self.filter.query_string}"
            verb = "GET"
            send_request(verb, path)

    instance = MyClass()
    instance.filter.filter = "prop1:value1 AND prop2:value2"
    instance.filter.max = 10
    instance.filter.offset = 5
    instance.filter.sort = "prop1,-prop2"
    instance.commit()
    ```
    """

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__
        self._committed: bool = False
        self._filter: str = None
        self._max: int = None
        self._offset: int = None
        self._query_string: str = None
        self._sort: str = None

    def commit(self) -> None:
        """Commit the query filter parameters"""
        params = {}
        if self._filter is not None:
            params["filter"] = self._filter
        if self._max is not None:
            params["max"] = self._max
        if self._offset is not None:
            params["offset"] = self._offset
        if self._sort is not None:
            params["sort"] = self._sort
        self._query_string = urlencode(params)
        self._committed = True

    @property
    def filter(self) -> str:
        """
        Lucene style filter string.  E.g. "prop1:value1 AND prop2:value2"

        Set (setter) or return (getter) the filter
        """
        return self._filter

    @filter.setter
    def filter(self, value: str) -> None:
        self._filter = value

    @property
    def max(self) -> int:
        """
        Maximum number of results to return.
        """
        return self._max

    @max.setter
    def max(self, value: int) -> None:
        self._max = value

    @property
    def offset(self) -> int:
        """
        Number of records to offset into the result set.
        """
        return self._offset

    @offset.setter
    def offset(self, value: int) -> None:
        self._offset = value

    @property
    def sort(self) -> str:
        """
        Comma separated list of properties to sort by.  Prefix with '-' for descending order.
        E.g. "prop1,-prop2"
        """
        return self._sort

    @sort.setter
    def sort(self, value: str) -> None:
        self._sort = value

    @property
    def query_string(self) -> str:
        """Return the query string"""
        method_name = inspect.stack()[0][3]
        if not self._committed:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.commit() must be called before accessing query_string"
            raise ValueError(msg)
        return self._query_string

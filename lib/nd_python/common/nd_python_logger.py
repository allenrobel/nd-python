from nd_python.common.log_v2 import Log


class NdPythonLogger(Log):
    """
    # Summary
    Configure logging for nd-python.

    # Usage example
    ```python
    NdPythonLogger()
    ```
    """

    def __init__(self):
        super().__init__()
        try:
            self.commit()
        except ValueError as error:
            msg = "Error while instantiating Log(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

class AlreadyProcessedException(Exception):
    """Exception raised when data has already been processed."""

    def __init__(self, message="Data has already been processed"):
        self.message = message
        super().__init__(self.message)


class InvalidOutputTypeError(Exception):
    """Exception raised when output text is not a string."""

    def __init__(self, output):
        self.output = output
        self.message = (
            f"Expected string type for output, got {type(output).__name__} instead."
        )
        super().__init__(self.message)

class GeneralException(Exception):
    """Base class for other exceptions.

    This class serves as a base class for creating custom exceptions. It takes
    an optional `exception_type` argument and an optional `msg` argument. If
    `exception_type` is not provided, it defaults to "GENERAL_EXCEPTION". If
    `msg` is not provided, it defaults to "General exception".
    """

    def __init__(self, exception_type=None, msg=None):
        self.exception_type = exception_type or "GENERAL_EXCEPTION"
        self.message = (
            f"[EXCEPTION: {self.exception_type}] {msg or 'General exception'}"
        )
        super().__init__(self.message)


class FileNotFoundException(GeneralException):
    """Exception raised when the file is missing.

    This exception is raised when a file that is expected to be present is not
    found. It takes an optional `msg` argument to provide more information
    about the error.
    """

    def __init__(self, msg=None):
        super().__init__("FILE_NOT_FOUND", msg)


class InvalidFileFormatException(GeneralException):
    """Exception raised when the file format is invalid.

    This exception is raised when the format of a file is not as expected. It
    takes an optional `msg` argument to provide more information about the
    error.
    """

    def __init__(self, msg=None):
        super().__init__("INVALID_FILE_FORMAT", msg)

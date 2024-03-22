class ApiException(Exception):
    def __init__(self, message="Api Exception"):
        super().__init__(message)


class BrowserException(Exception):
    def __init__(self, message="Browser Exception"):
        super().__init__(message)


class DataTableException(Exception):
    def __init__(self, message="Data Table Exception"):
        super().__init__(message)


class YearAscendingException(Exception):
    def __init__(self, message="Year Ascending Exception"):
        super().__init__(message)


class LocatorException(Exception):
    def __init__(self, message="Locator Exception"):
        super().__init__(message)


class DatasetHandlerException(Exception):
    def __init__(self, message="DatasetHandler Exception"):
        super().__init__(message)

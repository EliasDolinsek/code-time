class MonthDataFileNotFoundError(Exception):
    """Raised when file containing month data is not being found"""
    pass


class ConfigFileNotFoundError(Exception):
    """Raised when config file is not being found"""
    pass


class EmptyMonthDataError(Exception):
    """Raised when trying to write empty month data"""
    pass


class EmptyConfigError(Exception):
    """Raised when trying to write empty config"""
    pass


class InvalidMonthDataFileNameError(Exception):
    """Raised when trying to parse year from month data file name with an invalid file name"""
    pass

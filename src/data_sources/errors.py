class MonthDataFileNotFoundError(Exception):
    """Raised when file containing month data is not being found"""
    pass


class EmptyMonthDataError(Exception):
    """Raised when trying to write empty month data"""
    pass

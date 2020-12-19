class CodeTimeError(Exception):
    def __init__(self, message):
        super(CodeTimeError, self).__init__(message)


class MonthDataFileNotFoundError(CodeTimeError):
    """Raised when file containing month data is not being found"""

    def __init__(self, message="Could not load tracking data of month"):
        super(MonthDataFileNotFoundError, self).__init__(message)


class ConfigFileNotFoundError(CodeTimeError):
    """Raised when config file is not being found"""

    def __init__(self, message="Could not find config file"):
        super(ConfigFileNotFoundError, self).__init__(message)


class EmptyMonthDataError(CodeTimeError):
    """Raised when trying to write empty month data"""

    def __init__(self, message="Tried to write empty month data"):
        super(EmptyMonthDataError, self).__init__(message)


class EmptyConfigError(CodeTimeError):
    """Raised when trying to write empty config"""

    def __init__(self, message="Tried to write empty config"):
        super(EmptyConfigError, self).__init__(message)


class InvalidMonthDataFileNameError(CodeTimeError):
    """Raised when trying to parse year from month data file name with an invalid file name"""

    def __init__(self, message="Invalid name for month data file"):
        super(InvalidMonthDataFileNameError, self).__init__(message)


class DefaultSettingNotFoundError(CodeTimeError):
    """Raised when trying to get the default setting for an invalid settings-key"""

    def __init__(self, message="Invalid settings-key"):
        super(DefaultSettingNotFoundError, self).__init__(message)

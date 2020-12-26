class CodeTimeError(Exception):

    def __init__(self, message):
        """CodeTime specific errors."""
        super(CodeTimeError, self).__init__(message)


class MonthDataFileNotFoundError(CodeTimeError):

    def __init__(self, message="Could not load tracking data of month"):
        """Raised when file containing month data is not being found."""
        super(MonthDataFileNotFoundError, self).__init__(message)


class ConfigFileNotFoundError(CodeTimeError):

    def __init__(self, message="Could not find config file"):
        """Raised when config file is not being found."""
        super(ConfigFileNotFoundError, self).__init__(message)


class EmptyMonthDataError(CodeTimeError):

    def __init__(self, message="Tried to write empty month data"):
        """Raised when trying to write empty month data."""
        super(EmptyMonthDataError, self).__init__(message)


class EmptyConfigError(CodeTimeError):

    def __init__(self, message="Tried to write empty config"):
        """Raised when trying to write empty config."""
        super(EmptyConfigError, self).__init__(message)


class InvalidMonthDataFileNameError(CodeTimeError):

    def __init__(self, message="Invalid name for month data file"):
        """Raised when trying to parse year from month data file name with an invalid file name."""
        super(InvalidMonthDataFileNameError, self).__init__(message)


class DefaultSettingNotFoundError(CodeTimeError):

    def __init__(self, message="Invalid settings-key"):
        """Raised when trying to get the default setting for an invalid settings-key."""
        super(DefaultSettingNotFoundError, self).__init__(message)


class BackgroundImageNotFoundError(CodeTimeError):

    def __init__(self, message="Could not find background image"):
        """Raised when background image is not found."""
        super(BackgroundImageNotFoundError, self).__init__(message)


class UserImageNotFoundError(CodeTimeError):

    def __init__(self, message="Could not find user image"):
        """Raised when user image is not found."""
        super(UserImageNotFoundError, self).__init__(message)


class DataNotAvailableError(CodeTimeError):

    def __init__(self, message="No data available for the requested day"):
        """Raised when a specific month data is not available."""
        super(DataNotAvailableError, self).__init__(message)

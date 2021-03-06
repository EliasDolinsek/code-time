from pyautostart import SmartAutostart


class AutostartManager:

    def __init__(self, file: str):
        """Wrapper around pyautostart for enabling and disabling autostart."""
        self.autostart = SmartAutostart()
        self.name = "com.codetime"
        self.options = {
            "args": [file]
        }

    def enable(self):
        self.autostart.enable(self.name, self.options)

    def disable(self):
        self.autostart.disable(self.name)

    def is_enabled(self):
        return self.autostart.is_enabled(self.name)

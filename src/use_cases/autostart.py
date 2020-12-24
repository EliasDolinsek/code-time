from pyautostart import SmartAutostart


class AutostartManager:

    def __init__(self):
        self.autostart = SmartAutostart()
        self.name = "com.codetime"

    def enable(self):
        self.autostart.enable(self.name)

    def disable(self):
        self.autostart.disable(self.name)

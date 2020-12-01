import sys

if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace


class FocusActivityProvider:
    def get_activity_name(self) -> str:
        """Get name of the currently focused activity"""
        pass


class MacFocusActivityProvider(FocusActivityProvider):
    def get_activity_name(self) -> str:
        return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']


if __name__ == "__main__":
    activityProvider = MacFocusActivityProvider()
    print(activityProvider.get_activity_name())

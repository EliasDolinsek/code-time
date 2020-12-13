import sys
from abc import ABC, abstractmethod

if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace


class FocusActivityProvider(ABC):

    @abstractmethod
    def get_activity_name(self) -> str:
        """Get name of the currently focused activity"""
        pass


class MacFocusActivityProvider(FocusActivityProvider):
    def get_activity_name(self) -> str:
        return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']

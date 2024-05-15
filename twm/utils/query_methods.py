import xpybutil.ewmh as pyewmh
import xpybutil.window as Xwindow
import xcffib

from .config.confReader import confReader
from session_info import SessionInfo
from preferences import Preferences


class QueryMethods:
    def __init__(self):
        # Connection to The X Server
        self.connection = xcffib.connect()

        # Getting Available Screen
        self.screen = self.connection.get_setup().roots[0]

        self.colourmap = self.screen.default_colormap
        self.emwh = pyewmh
        self.root = self.screen.root

        self.prefs = Preferences
        self.session_info = SessionInfo

        self.config = confReader.read()

        self.window_resize_options = [
            "center",
            "maximize",
            "left",
            "right",
            "top",
            "bottom"
        ]
        self.managed_windows = []
        self.exposed_windows = []
        self.windowCount = int()
        self.last_raised_window = None
        self.active_window_title = self.session_info.session_name
        self.window_order = -1

        self.start = None
        self.attr = None

        self.deskbar = None

        self.wm_window_types = {
            "dock": '_NET_WM_WINDOW_TYPE_DOCK',
            "normal": '_NET_WM_WINDOW_TYPE_NORMAL',
            "dialog": '_NET_WM_WINDOW_TYPE_DIALOG',
            "utility": '_NET_WM_WINDOW_TYPE_UTILITY',
            "toolbar": '_NET_WM_WINDOW_TYPE_TOOLBAR',
            "menu": '_NET_WM_WINDOW_TYPE_MENU',
            "splash": '_NET_WM_WINDOW_TYPE_SPLASH'
        }
        self.wm_window_status = {
            "active": '_NET_ACTIVE_WINDOW',
            "desktop": '_NET_WM_DESKTOP',
            "above": '_NET_WM_STATE_ABOVE',
            "skip_taskbar": '_NET_WM_STATE_SKIP_TASKBAR',
            "maximize_vertical": '_NET_WM_STATE_MAXIMIZED_VERT',
            "maximize_horizontal": '_NET_WM_STATE_MAXIMIZED_HORIZ'
        }

    # Query Methods

    def getDesktop_Geometry(self):
        return pyewmh.get_desktop_geometry()

    def getWindow_Geometry(self, window):
        return Xwindow.get_geometry(window)

    def listWindows(self):
        return self.managed_windows

    def isWindow_Managed(self, window):
        return window in self.managed_windows

    def isWindow_Alive(self, window):
        if window not in self.managed_windows:
            return False
        else:
            return True

    def isWindow_Active(self, atom):
        if atom == self.wm_window_status["active"]:
            return True
        return False

    def getWindow_Active(self):
        window = None
        try:
            window = pyewmh.get_active_window()
        except:
            print("Failed to get Active Window.")
        return window

    def getWindow_Attr(self, event):
        try:
            return self.connection.core.GetWindowAttributes(event.window).reply()
        except:
            return None

    def getWindow_title(self, window):
        result = None
        try:
            result = pyewmh.get_wm_name(window)
        except:
            pass
        if result is None:
            return self.session_info.session_name
        return result

    def getWindow_State(self, window):
        return self.emwh.get_wm_state(window)

    def updateWindow_Count(self):
        if self.deskbar is not None:
            self.deskbar.set_window_count(len(self.managed_windows))
        else:
            self.windowCount += len(self.managed_windows)

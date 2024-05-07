from Xlib import X, display, XK, Xatom
import ewmh


class WindowManager():
    def __init__(self, prefs, session_info):
        #X Server Display and Screen init
        self.display = display.Display()
        self.screen = self.display.screen()
        self.colourmap = self.screen.default_colormap
        self.emwh = ewmh.EWMH()
        self.root = self.screen.root

        self.prefs = prefs

        self.display_dimensions = self.get_display_geometry()
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
        self.last_raised_window = None
        self.active_window_title = self.session_info.session_name
        self.window_order = -1

        self.key_alias = {}
        self.keys_down = set()
        self.current_modifier_keys = set()

        self.start = None
        self.attr = None

        self.wm_window_type = self.display.intern_atom('_NET_WM_WINDOW_TYPE')
        self.wm_state = self.display.intern_atom('_NET_WM_STATE')
        self.wm_window_types = {
            "dock": self.display.intern_atom('_NET_WM_WINDOW_TYPE_DOCK'),
            "normal": self.display.intern_atom('_NET_WM_WINDOW_TYPE_NORMAL'),
            "dialog": self.display.intern_atom('_NET_WM_WINDOW_TYPE_DIALOG'),
            "utility": self.display.intern_atom('_NET_WM_WINDOW_TYPE_UTILITY'),
            "toolbar": self.display.intern_atom('_NET_WM_WINDOW_TYPE_TOOLBAR'),
            "menu": self.display.intern_atom('_NET_WM_WINDOW_TYPE_MENU'),
            "splash": self.display.intern_atom('_NET_WM_WINDOW_TYPE_SPLASH')
        }
        self.wm_window_status = {
            "active": self.display.intern_atom('_NET_ACTIVE_WINDOW'),
            "desktop": self.display.intern_atom('_NET_WM_DESKTOP'),
            "above": self.display.intern_atom('_NET_WM_STATE_ABOVE'),
            "skip_taskbar": self.display.intern_atom('_NET_WM_STATE_SKIP_TASKBAR'),
            "maximize_vertical": self.display.intern_atom('_NET_WM_STATE_MAXIMIZED_VERT'),
            "maximize_horizontal": self.display.intern_atom('_NET_WM_STATE_MAXIMIZED_HORIZ')
        }

    # Query Methods

    def listWindows(self):
        return self.display_root.query_tree().children
    
    def isWindow_Managed(self, window):
        return window in self.managed_windows
    
    def isWindow_Alive(self, window):
        windows = self.display_root.query_tree().children
        return window in windows

    def isWindow_Active(self, atom):
        if atom == self.wm_window_status["active"]:
            return True
        return False

    def getWindow_Active(self):
        window = None
        try:
            window = self.display_root.get_full_property(self.wm_state["active", Xatom.ATOM])
        except:
            print("Failed to get Active Window.")
        return window
    
    def getWindow_Attr(self, window):
        try:
            return window.get_attributes()
        except:
            return None

    def getWindow_shortName(self, window):
            return '0x{:x} [{}]'.format(window.id, self.getWindow_Class(window))


    def getWindow_title(self, window):
        result = None
        try:
            result = window.get_wm_name()
        except:
            pass
        if result is None:
            return self.session_info.session_name
        return result


    def getWindow_State(self, window):
        return self.ewmh.getWmState(window, str = True)

    def updateWindow_Count(self):
        if self.deskbar is not None:
            self.deskbar.set_window_count(len(self.managed_windows))


    # Window Controls

    def manageWindow(self, window):
        attr = self.getWindow_Attr(window)
        if attr is None:
            return
        if attr.override_redirect:
            return
        if self.managed_windows(window):
            return
        
        if self.prefs.dev["debug"] == 1:
            print("Window Found: %s", self.getWindow_shortName(window))
        self.managed_windows.append(window)
        self.exposed_windows.append(window)
        self.window_order = len(self.managed_windows) - 1
        self.updateWindow_Count()

        window.map()
        mask = X.EnterWindowMask | X.LeaveWindowMask
        
    
    def unmanageWindow(self, window):
        if self.isWindow_Managed(window):
            if self.prefs.dev["debug"] == 1:
                print("Unmanaging window: %s", self.getWindow_shortName(window))
            if window in self.managed_windows:
                self.managed_windows.remove(window)
                self.window_order = len(self.managed_windows) - 1
                self.updateWindow_Count()
            if window in self.exposed_windows:
                self.exposed_windows.remove(window)
    
    def destroyWindow(self, window):
        if self.prefs.dev["debug"] == 1:
                print("Destroy window: %s", self.get_window_shortname(window))
        if self.isWindow_Managed(window):
            window.destroy()
            self.unmanage_window(window)

from Xlib import X, display, XK, Xatom
import ewmh

class WindowManager():
    def __init__(self):
        #X Server Display and Screen init
        self.display = display.Display()
        self.screen = self.display.screen()
        self.colourmap = self.screen.default_colormap
        self.emwh = ewmh.EWMH()
        self.root = self.screen.root

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

    # Window Controls

    def window_manage(self, window):
        raise NotImplementedError
    
    def window_unmanage(self, window):
        raise NotImplementedError
    
    def window_destroy(self, window):
        raise NotImplementedError
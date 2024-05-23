import xcffib
import xcffib.xproto
import sys

from ..utils.query_methods import QueryMethods
from ..utils.logUtils import logger

# Pre Defined Constants to be used in Window Manager
NXT_WIN = "NEXT_WINDOW"
PREV_WIN = "PREVIOUS_WINDOW"

sys.path.append("/home/Legendyboi/")


class WindowManager(QueryMethods):
    super().__init__()

    # Window Controls
    def mapWindow(self, event):
        """
            To make itself visible, a Window will send `MapRequestEvent` that gets sent to the window manager.
            In this Function, we add the window to our managed windows list and tell the X server to make it visible.
            :param event: Handling MapRequestEvent
        """

        window = event.window
        attr = self.getWindow_Attr(window)

        if attr is None:
            return
        if attr.override_redirect:
            return
        if self.managed_windows(window):
            return

        if self.prefs.dev["debug"] == 1:
            logger.debug("Window Mapped: %s", self.getWindow_title(window))

        self.connection.core.MapWindow(event.window)
        self.connection.core.ConfigureWindow(
            event.window,
            xcffib.xproto.ConfigWindow.X |
            xcffib.xproto.ConfigWindow.Y |
            xcffib.xproto.ConfigWindow.Width |
            xcffib.xproto.ConfigWindow.Height,
            [
                100,  # X position
                100,  # Y position
                800,  # Width
                600  # Height
            ]
        )

        self.managed_windows.append(window)
        self.exposed_windows.append(window)
        self.window_order = len(self.managed_windows) - 1
        self.updateWindow_Count()

    def configureRequests(self, event):
        """
            A request that asks to change something about a window.
            May include width/height, x/y, border width/color, and more
        :param event: Handling ConfigureRequestEvent
        """
        self.connection.core.ConfigureWindow(
            event.window,
            xcffib.xproto.ConfigWindow.X |
            xcffib.xproto.ConfigWindow.Y |
            xcffib.xproto.ConfigWindow.Width |
            xcffib.xproto.ConfigWindow.Height |
            xcffib.xproto.ConfigWindow.BorderWidth |
            xcffib.xproto.ConfigWindow.Sibling |
            xcffib.xproto.ConfigWindow.StackMode,
            [
                event.x,
                event.y,
                event.width,
                event.height,
                event.border_width,
                event.sibling,
                event.stack_mode
            ]
        )

    def unmanageWindow(self, event):
        window = event.window
        if self.isWindow_Managed(window):
            if self.prefs.dev["debug"] == 1:
                logger.debug("Unmanaging window: %s", self.getWindow_title(window))
            if window in self.managed_windows:
                self.managed_windows.remove(window)
                self.window_order = len(self.managed_windows) - 1
                self.updateWindow_Count()
            if window in self.exposed_windows:
                self.exposed_windows.remove(window)

    def destroyWindow(self, event):
        window = event.window
        if self.prefs.dev["debug"] == 1:
            logger.debug("Destroyed window: %s", self.getWindow_title(window))
        if self.isWindow_Managed(window):
            self.unmanageWindow(window)

    def run(self):

        cookie = self.connection.core.ChangeWindowAttributesChecked(
            self.root,
            xcffib.xproto.CW.EventMask,
            [
                xcffib.xproto.EventMask.SubstructureNotify |
                xcffib.xproto.EventMask.SubstructureRedirect,
            ]
        )

        try:
            cookie.check()
        except:
            logger.error(logger.traceback.format_exc())
            print('Is another window manager running?')
            exit()
        finally:
            logger.info("Cookie is correct.")

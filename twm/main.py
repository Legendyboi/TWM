from components.window_manager import WindowManager
import os

class SessionInfo(object):
    def __init__(self):
        self.session_name = "LigindiXWM"
        self.kernel_version = os.popen('uname -rm').read()[:-1]
    
class Preferences(object):
    def __init__(self):
        self.dev = {
            "debug": 1
        }

WindowManager(prefs= Preferences, session_info=SessionInfo)

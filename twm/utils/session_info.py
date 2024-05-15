import os


class SessionInfo(object):
    def __init__(self):
        self.session_name = "LigindiXWM"
        self.kernel_version = os.popen('uname -rm').read()[:-1]

from config.confReader import confReader

config = confReader().read()


class Preferences:
    def __init__(self):
        self.dev = config.get('dev', False)
        self.warning = config.get('warn', False)

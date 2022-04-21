from app.settings import logger


class Log:
    def __init__(self, msg):
        if logger.enable:
            print("\n🦋 " + msg + "\n")

import subprocess

class CommandLine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CommandLine, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        pass


MAIN_CMD = CommandLine()

if __name__ == "__main__":
    MAIN_CMD = CommandLine()
import subprocess

class CommandLine:
    _instace = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CommandLine, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def init(self):
        if self._initialized:
            return
        
        self.cmd = subprocess.Popen('powershell.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        self._initialized = True

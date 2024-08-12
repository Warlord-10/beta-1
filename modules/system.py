from modules.logger import MAIN_LOGGER

# Holds the system information
class System:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):  

        self.logger = MAIN_LOGGER
        self.screenshot_path = "./screenshot/screenshot.png"
        self.curr_path = "C:/Users/deepa/Desktop"
        self.last_prompt = None


    def getLastPrompt(self):
        return self.last_prompt
    
    def setLastPrompt(self, prompt):
        self.last_prompt = prompt

    def changeCurrentPath(self, path):
        self.curr_path = path

    def getCurrentPath(self):
        return self.curr_path
    
Environment = System()
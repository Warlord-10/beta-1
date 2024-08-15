import os

# Holds the system information
class System:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):  
        self.MAIN_LLM = None
        self.MAIN_MEMORY = None

        # Personal details
        self.user_name = "DJ"
        self.email = "random@gmail.com"

        # Settings
        self.should_speak = False
        self.should_function_call = True
        self.screenshot_path = "./screenshot/screenshot.png"
        self.default_working_directory = os.getcwd()
        self.curr_path = os.getcwd()
        self.verbose = False

    def setMemory(self, memory):
        self.MAIN_MEMORY = memory
    def setLLMModel(self, model):
        self.MAIN_LLM = model


    def getUserDetails(self):
        return {
            "name": self.user_name,
            "email": self.email
        }
    def setUserDetails(self, *args, **kwargs):
        self.user_name = kwargs["name"]
        self.email = kwargs["email"]


    def getSettings(self):
        return {
            "should_speak": self.should_speak,
            "should_function_call": self.should_function_call,
            "screenshot_path": self.screenshot_path,
            "default_working_directory": self.default_working_directory,
            "curr_path": self.curr_path
        }
    def setSettings(self, *args, **kwargs):
        self.should_speak = kwargs["should_speak"]
        self.should_function_call = kwargs["should_function_call"]


    def setCurrentPath(self, path):
        self.curr_path = path

    def getCurrentPath(self):
        return self.curr_path
    
Environment = System()
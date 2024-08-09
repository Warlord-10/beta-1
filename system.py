class System:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.curr_path = "C:/Users/deepa/Desktop"

        self._initialized = True


    def changeCurrentPath(self, path):
        self.curr_path = path

    def getCurrentPath(self):
        return self.curr_path
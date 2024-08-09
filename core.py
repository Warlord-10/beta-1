import threading
import queue
import inspect
import tools.FileManager as FileManagerTools

class Core:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Core, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        # Initialization begins 

        self.FUNCTIONS = self.__loadFunctions()

        self.task_queue = queue.Queue()
        self.objective_ID = None

        self.taskExecutionSignal = threading.Event()
        self.taskQueueThread = threading.Thread(target=self.__processQueue, daemon=True)
        self.taskQueueThread.start()


        # Initialization ends
        self._initialized = True

    def addTask(self, task):
        self.task_queue.put(task)
        if not self.taskExecutionSignal.is_set():
            self.taskExecutionSignal.set()

    def getTask(self):
        return self.task_queue.get()
    
    def __loadFunctions(self):
        functions_dict = {}
        modules = [FileManagerTools]
        for module in modules:
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith('_'):
                    functions_dict[name] = obj

        return functions_dict
    
    def __processQueue(self):
        while True:
            # Wait for a signal that tasks are available
            self.taskExecutionSignal.wait()

            while self.task_queue:
                try:
                    task = self.getTask()
                    self.__executeTask(task)
                except Exception as e:
                    break
            
            # Reset the event
            self.taskExecutionSignal.clear()


    def __executeTask(self, task):
        print("Executing task")
        curr_task_name = task["fn_name"]
        curr_task_kwargs = task["kwargs"]

        try:
            function_to_call = self.FUNCTIONS[curr_task_name]
            function_to_call(**curr_task_kwargs)
        except:
            pass



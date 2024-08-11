import threading
import queue
import inspect
import uuid

from system import Environment

import tools.FileManager as FileManagerTools
import tools.Operations as OperationsTools
from llm import MAIN_LLM as LlmTools




# Used for managing the tasks, and executing them
class Core:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Core, cls).__new__(cls)
            cls._instance._initialize(cls, *args, **kwargs)
        return cls._instance

     # Private functions
    def _initialize(self):
        self.FUNCTIONS = self._loadFunctions()

        self.task_queue = queue.Queue()

        self.taskExecutionSignal = threading.Event()
        self.taskQueueThread = threading.Thread(target=self._processQueue, daemon=True)
        self.taskQueueThread.start()

        Environment.logger.info("Core initialized successfully")

    def _loadFunctions(self):
        functions_dict = {}
        modules_and_classes = [
            FileManagerTools,
            OperationsTools,
            LlmTools
        ]

        for item in modules_and_classes:
            if inspect.ismodule(item):
                for name, obj in inspect.getmembers(item):
                    if inspect.isfunction(obj) and not name.startswith("_"):
                        functions_dict[name] = obj
                
            elif inspect.isclass(item):
                for name, obj in inspect.getmembers(item):
                    if inspect.isfunction(obj) and not name.startswith("_"):
                        functions_dict[name] = obj
            else:
                for name, obj in inspect.getmembers(item):
                    if inspect.ismethod(obj) and not name.startswith("_"):
                        functions_dict[name] = obj

        # print(functions_dict.keys())
        return functions_dict
    
    def _processQueue(self):
        while True:
            # Wait for a signal that tasks are available
            self.taskExecutionSignal.wait()

            while self.task_queue:
                try:
                    task = self.getTask()
                    self._executeTask(task)
                except Exception as e:
                    break
            
            # Reset the event
            self.taskExecutionSignal.clear()

    def _executeTask(self, task):
        # print("Executing task: ", task["id"], task["fn_name"])
        curr_task_name = task["fn_name"]
        curr_task_kwargs = task["kwargs"]

        try:
            function_to_call = self.FUNCTIONS[curr_task_name]
            function_to_call(**curr_task_kwargs)
        except Exception as e:
            print(e)


    # Public functions
    def addTask(self, task):
        task["id"] = uuid.uuid4()
        self.task_queue.put(task)
        if not self.taskExecutionSignal.is_set():
            self.taskExecutionSignal.set()

    def getTask(self):
        return self.task_queue.get()
    
MAIN_CORE = Core()

if __name__ == "__main__":
    MAIN_CORE = Core()
    



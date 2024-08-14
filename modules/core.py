import threading
import queue
import inspect
import uuid

from modules.logger import MAIN_LOGGER
from modules.speech import MAIN_SPEECH
from modules.event_dispatcher import EventDispatcher
from modules.llm import GroqLLM

# Importing all the tools
from modules.memory import KnowledgeBase
from modules.system import Environment

import tools.FileManager as FileManagerTools
import tools.Operations as OperationsTools
import tools.InformationProvider as LlmTools
import tools.browser as BrowserTools

modules_and_classes = [
    FileManagerTools,
    OperationsTools,
    LlmTools,
    Environment.MAIN_MEMORY,
    BrowserTools
]


# Used for managing the tasks, and executing them
class Core:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Core, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

     # Private functions
    def _initialize(self):
        self.FUNCTIONS = self._loadFunctions()

        self.task_queue = queue.Queue()

        self.dispatcher = EventDispatcher()
        self.dispatcher.subscribe('LLM_RESPONSE', self.createTask)

        self.taskExecutionSignal = threading.Event()
        self.taskQueueThread = threading.Thread(target=self._processQueue, daemon=True)
        self.taskQueueThread.start()

        MAIN_LOGGER.info("Core initialized successfully")

    def _loadFunctions(self):
        functions_dict = {}

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

        print(functions_dict.keys())
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
        print("Executing task: ", task["id"], task["fn_name"])
        curr_task_name = task["fn_name"]
        curr_task_kwargs = task["kwargs"]

        try:
            function_to_call = self.FUNCTIONS[curr_task_name]
            function_to_call(**curr_task_kwargs)
        except Exception as e:
            print(e)



    # Public functions
    def createTask(self, response):
        if isinstance(Environment.MAIN_LLM, GroqLLM):
            print(response)
            MAIN_SPEECH.speak(response.content)
            return 
        
        for part in response.parts:
            if fn := part.function_call:    
                kwargs = {}
                for key, val in fn.args.items():
                    kwargs[key] = val
                task = {
                    "id": uuid.uuid4(),
                    "fn_name": fn.name,
                    "kwargs": kwargs
                }
                self.addTask(task)
            
            elif fn := part.text:
                print("\n[Beta-1]: ", fn.format())
                MAIN_SPEECH.speak(fn.format())

    def addTask(self, task):
        self.task_queue.put(task)
        if not self.taskExecutionSignal.is_set():
            self.taskExecutionSignal.set()

    def getTask(self):
        return self.task_queue.get()
    

if __name__ == "__main__":
    MAIN_CORE = Core()
    



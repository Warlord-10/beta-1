"""
        +-----------------------+
        |      Environment      |
        |  (Entry Point & Main  |
        |  Coordinator)         |
        +-----------------------+
            |          |          \
            |          |           \
            |          |            \
        +------+    +------+     +---------+
        | Core |    | LLM  |     |  OS     |
        |      |    |      |     |         |
        +------+    +------+     +---------+
            |           |            
            |           |            
            |           |            
        +-----------+   |            
        | Task Queue|   |            
        | (in Core) |   |            
        +-----------+   |            
                        |           
                        |            
                        v            
                    +---------------+
                    |  Memory       |
                    |  Module       |
                    +---------------+
"""               

from modules.core import MAIN_CORE
from modules.llm import MAIN_LLM
from modules.system import Environment


class BetaEnvironment:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BetaEnvironment, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        Environment.logger.info("Beta-1 Environment initialized successfully")


    def run(self):
        while True:
            prompt = MAIN_LLM.takeTextInput()
            if prompt == "exit":
                break

            response = MAIN_LLM.sendPrompt(prompt)

            # Parse the response and add tasks
            for part in response.parts:
                if fn := part.function_call:
                    
                    kwargs = {}
                    for key, val in fn.args.items():
                        kwargs[key] = val

                    function_definition = {
                        "fn_name": fn.name,
                        "kwargs": kwargs
                    }

                    MAIN_CORE.addTask(function_definition)
                elif fn := part.text:
                    print(fn.format())



if __name__ == "__main__":
    # COMPLETED: file management
    # TODO: 
    mainObj = BetaEnvironment()
    mainObj.run()

    pass


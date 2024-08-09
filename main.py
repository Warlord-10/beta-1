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

import core
import llm
import logger
import tools.operations as operations

MAIN_LOGGER = logger.LoggerSetup().get_logger()
MAIN_CORE = core.Core()
MAIN_LLM = llm.Llm()

class BetaEnvironment:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BetaEnvironment, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        MAIN_LOGGER.info("Beta Environment initialized successfully")

        self._initialized = True

    def run(self):
        while True:
            prompt = input("Prompt: ")
            if prompt == "exit":
                break

            response = MAIN_LLM.getResponse(prompt)
            print(response)


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

                    # MAIN_CORE.addTask(function_definition)
                elif fn := part.text:
                    print(fn.format())



if __name__ == "__main__":
    mainObj = BetaEnvironment()
    mainObj.run()



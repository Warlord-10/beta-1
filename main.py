
from modules.core import Core
from modules.llm import GroqLLM, GoogleLLM
from modules.logger import MAIN_LOGGER
from modules.system import Environment
from modules.memory import KnowledgeBase



class BetaEnvironment:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BetaEnvironment, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        # llm = GoogleLLM()
        llm = GroqLLM()
        mem = KnowledgeBase()

        Environment.setLLMModel(llm)
        Environment.setMemory(mem)
        core = Core()

        print(f"\n{Environment.getSettings()}")
        MAIN_LOGGER.info("Beta-1 Environment initialized successfully")


    def run(self):
        while True:
            prompt = input("Prompt: ")
            if prompt == "exit":
                break
            elif prompt == "~settings":
                print(Environment.getSettings())
            elif prompt == "~user":
                print(Environment.getUserDetails())
            else:
                response = Environment.MAIN_LLM.sendPrompt(prompt)
            



if __name__ == "__main__":
    # COMPLETED: file management
    # TODO: 
    mainObj = BetaEnvironment()
    mainObj.run()

    pass


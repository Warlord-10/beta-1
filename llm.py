"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import google.generativeai as genai
from PIL import Image
import logger
from config import FILE_MANAGER_FUNC_DECL


class Llm:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Llm, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.LOGGER = logger.LoggerSetup().get_logger()
        genai.configure(api_key="AIzaSyBj5Y8YUwT1oa-JNJLkYN3jTR6eA-dORbY")

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain"
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            system_instruction="""
                your name is Beta-1
                
                As a smart assistant, you have full control over the mouse and keyboard of this computer. You are going to use these function just like a human being. 
                So select the next best sequence of actions to perform which will complete the objective. 
                If you face any doubt, feel free to ask the user for it.
                
                Remember to provide the reason for chosing the action. 
            """,

            tools=[{
                "function_declarations": FILE_MANAGER_FUNC_DECL
            }],

            tool_config={
                "function_calling_config": {"mode": "AUTO"}
            }
        )

        # print(self.model._tools.to_proto())

        self.CHAT_SESSION = self.model.start_chat(
            history=[], 
            enable_automatic_function_calling=False
        )
        self.LOGGER.info("LLM initialized successfully")
    

        self._initialized = True

    def generateContent(self, message):
        response = self.model.generate_content([message, Image.open("screenshot/screenshot.png")])
        return response

    def getResponse(self, message):
        response = self.CHAT_SESSION.send_message(message)
        return response
    

if __name__ == "__main__":
    MAIN_LLM = Llm()
    while True:
        prompt = input("Prompt: ")
        if prompt == "exit":
            break

        # Take the screenshot
        # operations.take_screenshot()

        response = MAIN_LLM.getResponse(prompt)
        print(response)

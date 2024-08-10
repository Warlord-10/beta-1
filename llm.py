"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from PIL import Image
from system import Environment
from config import (
    FILE_MANAGER_FUNC_DECL,
    OPERATIONS_FUNC_DECL,
    LLM_FUNC_DECL
)


# Actual llm class
class Llm:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Llm, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance
    
    def _initialize(self):
        genai.configure(api_key="AIzaSyBj5Y8YUwT1oa-JNJLkYN3jTR6eA-dORbY")

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain"
        }
        safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction="""
                Your name is Beta-1
                
                - As a smart assistant, you are given lots of APIs to control the computer. 
                
                - Your role is to analyze the objective and then divide it into subtasks which can be completed by a single API calls. Then combine all the API calls to complete the whole objective.

                - Your approach must follow the divide and conquer approach towards the objective.
                
                - sendPrompt function must be called ONLY when the model requires extra data from the machine. This must not be used for regular answer generation.

                - If you face any doubt, feel free to ask the user for it.
                - Return the array of function calls you need to make to finish the objective.
                - Remember to always provide the reason for chosing the API. 
            """,

            tools=[{
                "function_declarations": FILE_MANAGER_FUNC_DECL+OPERATIONS_FUNC_DECL+LLM_FUNC_DECL
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
        Environment.logger.info("LLM initialized successfully")

    # Main functions for interacting with the model
    def generateContent(self, message):
        response = self.model.generate_content([message, Image.open("screenshot/screenshot.png")])
        return response

    def sendPrompt(self, message, image_path=None):
        if image_path is None:
            response = self.CHAT_SESSION.send_message(message)
        else:
            response = self.CHAT_SESSION.send_message([message,Image.open(image_path)])
        print(response)
        return response
    
MAIN_LLM = Llm()



if __name__ == "__main__":
    MAIN_LLM = Llm()
    while True:
        prompt = input("Prompt: ")
        if prompt == "exit":
            break

        # Take the screenshot
        # operations.take_screenshot()

        response = MAIN_LLM.sendPrompt(prompt)

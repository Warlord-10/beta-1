import os
import google.generativeai as genai

from config import *
from PIL import Image
from groq import Groq
from modules.logger import MAIN_LOGGER
from modules.event_dispatcher import EventDispatcher
from google.generativeai.types import HarmCategory, HarmBlockThreshold


# Base LLM class
class Llm:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Llm, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        self.system_prompt = """
            Your name is Beta-1
            - As a smart assistant, you are given lots of APIs to control the computer and complete the task. 
            - If you face any doubt, feel free to ask the user for it. While executing a function, if you need extra details from me, just ASK.
            - Remember to always provide the reason for chosing the API. 
        """
        self.tools = FILE_MANAGER_FUNC_DECL + OPERATIONS_FUNC_DECL + LLM_FUNC_DECL + MEMORY_FUNC_DECL + BROWSER_FUNC_DECL
        self.dispatcher = EventDispatcher()

    def takeTextInput(self):
        prompt = input("Prompt: ")
        return prompt

    def sendPrompt(self, message, image_path=None):
        # To be overridden by subclasses
        raise NotImplementedError("sendPrompt method must be overridden by subclass")

# Google Gemini LLM class
class GoogleLLM(Llm):
    def _initialize(self):
        super()._initialize()
        genai.configure(api_key=os.environ.get("GEMINI_API"))

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 4096,
            "response_mime_type": "text/plain"
        }
        safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=self.system_prompt,

            tools=[{
                "function_declarations": self.tools
            }],

            tool_config={
                "function_calling_config": {"mode": "AUTO"}
            }
        )

        self.CHAT_SESSION = self.model.start_chat(
            history=[], 
            enable_automatic_function_calling=False
        )
        MAIN_LOGGER.info("Gemini LLM initialized successfully")

    def sendPrompt(self, message, image_path=None):
        if image_path is None:
            response = self.CHAT_SESSION.send_message(message)
        else:
            response = self.CHAT_SESSION.send_message([message, Image.open(image_path)])

        self.dispatcher.publish('LLM_RESPONSE', response)
        return response


# Groq LLM class inheriting from Llm
class GroqLLM(Llm):
    def _initialize(self):
        super()._initialize()
        self.model = Groq(api_key=os.environ.get("GROQ_API"))

        MAIN_LOGGER.info("Gorq LLM initialized successfully")

    def sendPrompt(self, message):
        response = self.model.chat.completions.create(
            model="gemma2-9b-it",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": message,
                }
            ],
            # tools=[FILE_MANAGER_FUNC_DECL + OPERATIONS_FUNC_DECL + LLM_FUNC_DECL + MEMORY_FUNC_DECL],
            # tool_choice="auto",
            max_tokens=4096
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        self.dispatcher.publish('LLM_RESPONSE', response_message)
        # print(response_message.content)
        # print(response_message)
        


if __name__ == "__main__":
    llm_choice = input("Choose LLM (1 for Google, 2 for Groq): ")
    if llm_choice == "1":
        MAIN_LLM = GoogleLLM()
    elif llm_choice == "2":
        MAIN_LLM = GroqLLM()
    else:
        print("Invalid choice, exiting.")
        exit(1)

    while True:
        prompt = input("Prompt: ")
        if prompt.lower() == "exit":
            break

        response = MAIN_LLM.sendPrompt(prompt)

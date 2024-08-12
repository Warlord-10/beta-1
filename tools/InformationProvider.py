from modules.llm import MAIN_LLM
from tools.Operations import take_screenshot

# def send_information_to_LLM(prompt):
#     MAIN_LLM.sendPrompt(prompt)

def analyze_screen():
    take_screenshot()
    MAIN_LLM.sendPrompt(message="Here is the screen for analysis", image_path="screenshot/screenshot.png")
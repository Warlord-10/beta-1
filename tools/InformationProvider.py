from modules.system import System
from tools.Operations import take_screenshot

# def send_information_to_LLM(prompt):
#     response = MAIN_LLM.sendPrompt(prompt)
#     return response.text


Environment = System()

def analyze_screen():
    take_screenshot()
    response = Environment.MAIN_LLM.sendPrompt(message="Here is the screen for analysis", image_path="screenshot/screenshot.png")
    print(response.text)
    return response.text
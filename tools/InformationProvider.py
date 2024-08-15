import os
from modules.system import Environment
from tools.Operations import take_screenshot

def analyze_screen():
    take_screenshot()
    response = Environment.MAIN_LLM.sendPrompt(message="Here is the screen for analysis", image_path="screenshot/screenshot.png")

def analyze_file(file_path):
    if os.path.basename(file_path) == file_path:
        file_path = os.path.join(Environment.getCurrentPath(), file_path)
    with open(file_path, "r") as file:
        file_content = file.read()
        response = Environment.MAIN_LLM.sendPrompt(message=f"Here is the file for analysis:\n{file_content}")
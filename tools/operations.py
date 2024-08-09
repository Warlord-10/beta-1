from typing import Iterable, Sequence
import pyautogui
from PIL import Image
import time
import logger

LOGGER = logger.LoggerSetup().get_logger()

# Set a small pause between PyAutoGUI commands for stability
pyautogui.PAUSE = 0.1

# Enable fail-safe (move mouse to upper-left corner to abort)
pyautogui.FAILSAFE = True
    
    
def move_mouse(x_percent, y_percent) -> None:
    """Move the mouse to the specified coordinates."""
    try:
        screen_width, screen_height = pyautogui.size()
        x = int(screen_width * x_percent)
        y = int(screen_height * y_percent)
        pyautogui.moveTo(x, y)
        LOGGER.info(f"Moved mouse to position ({x_percent}, {y_percent}) of the screen")
    except Exception as e:
        LOGGER.error(f"Failed to move mouse: {str(e)}")

def click_mouse(x, y) -> None:
    """Click the mouse at the current position or specified coordinates."""
    try:
        if x is not None and y is not None:
            pyautogui.click(x, y)
            LOGGER.info(f"Clicked mouse at position ({x}, {y})")
        else:
            pyautogui.click()
            LOGGER.info("Clicked mouse at current position")
    except Exception as e:
        LOGGER.error(f"Failed to click mouse: {str(e)}")

def type_text(text) -> None:
    """Type the specified text."""
    try:
        pyautogui.typewrite(text)
        LOGGER.info(f"Typed text: {text}")
    except Exception as e:
        LOGGER.error(f"Failed to type text: {str(e)}")

def press_key(key) -> None:
    """Press the specified key."""
    try:
        pyautogui.press(key)
        LOGGER.info(f"Pressed key: {key}")
    except Exception as e:
        LOGGER.error(f"Failed to press key: {str(e)}")



def take_screenshot(filename:str="screenshot.png") -> None:
    """Take a screenshot of the entire screen."""
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot/" + filename)

        LOGGER.info(f"Saved screenshot as {filename}")
        return filename
    except Exception as e:
        LOGGER.error(f"Failed to take screenshot: {str(e)}")
        return None

def take_region_screenshot(region:tuple[int, int, int, int], filename:str="screenshot.png") -> None:
    """Take a screenshot of a specific region."""
    try:
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save("screenshot/" + filename)

        LOGGER.info(f"Saved region screenshot as {filename}")
        return filename
    except Exception as e:
        LOGGER.error(f"Failed to take region screenshot: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    move_mouse(100, 100)
    click_mouse()
    type_text("Hello, JARVIS!")
    press_key('enter')
    take_screenshot()
    take_region_screenshot((0, 0, 300, 300), "region_shot.png")
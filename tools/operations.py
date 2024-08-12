import pyautogui
import modules.logger as logger

from modules.system import Environment

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
        Environment.logger.info(f"Moved mouse to position ({x_percent}, {y_percent}) of the screen")
    except Exception as e:
        Environment.logger.error(f"Failed to move mouse: {str(e)}")

def click_mouse(x, y) -> None:
    """Click the mouse at the current position or specified coordinates."""
    try:
        if x is not None and y is not None:
            pyautogui.click(x, y)
            Environment.logger.info(f"Clicked mouse at position ({x}, {y})")
        else:
            pyautogui.click()
            Environment.logger.info("Clicked mouse at current position")
    except Exception as e:
        Environment.logger.error(f"Failed to click mouse: {str(e)}")

def type_text(text) -> None:
    """Type the specified text."""
    try:
        pyautogui.typewrite(text)
        Environment.logger.info(f"Typed text: {text}")
    except Exception as e:
        Environment.logger.error(f"Failed to type text: {str(e)}")

def press_key(key) -> None:
    """Press the specified key."""
    try:
        pyautogui.press(key)
        Environment.logger.info(f"Pressed key: {key}")
    except Exception as e:
        Environment.logger.error(f"Failed to press key: {str(e)}")



def take_screenshot(filename=None):
    """Take a screenshot of the entire screen."""
    try:
        if filename is None:
            filename = "screenshot.png"

        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot/" + filename)

        Environment.logger.info(f"Saved screenshot as {filename}")
        return filename
    except Exception as e:
        Environment.logger.error(f"Failed to take screenshot: {str(e)}")
        return None

def take_region_screenshot(region:tuple[int, int, int, int], filename:str="screenshot.png") -> None:
    """Take a screenshot of a specific region."""
    try:
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save("screenshot/" + filename)

        Environment.logger.info(f"Saved region screenshot as {filename}")
        return filename
    except Exception as e:
        Environment.logger.error(f"Failed to take region screenshot: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    move_mouse(100, 100)
    click_mouse()
    type_text("Hello, JARVIS!")
    press_key('enter')
    take_screenshot()
    take_region_screenshot((0, 0, 300, 300), "region_shot.png")
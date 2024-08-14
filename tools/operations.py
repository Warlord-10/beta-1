import pyautogui


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
    except Exception as e:
        return
    
def click_mouse(x, y) -> None:
    """Click the mouse at the current position or specified coordinates."""
    try:
        if x is not None and y is not None:
            pyautogui.click(x, y)
            Environment.logger.info(f"Clicked mouse at position ({x}, {y})")
        else:
            pyautogui.click()
    except Exception as e:
        return
    
def type_text(text) -> None:
    """Type the specified text."""
    try:
        pyautogui.typewrite(text)
    except Exception as e:
        return 
    
def press_key(key) -> None:
    """Press the specified key."""
    try:
        pyautogui.press(key)
    except Exception as e:
        return


def take_screenshot(filename=None):
    """Take a screenshot of the entire screen."""
    try:
        if filename is None:
            filename = "screenshot.png"

        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot/" + filename)

        return filename
    except Exception as e:
        return None

def take_region_screenshot(region:tuple[int, int, int, int], filename:str="screenshot.png") -> None:
    """Take a screenshot of a specific region."""
    try:
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save("screenshot/" + filename)

        return filename
    except Exception as e:
        return None


# Example usage
if __name__ == "__main__":
    move_mouse(100, 100)
    click_mouse()
    type_text("Hello, JARVIS!")
    press_key('enter')
    take_screenshot()
    take_region_screenshot((0, 0, 300, 300), "region_shot.png")
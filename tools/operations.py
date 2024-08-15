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
        return "mouse moved"
    except Exception as e:
        return str(e)
    
def click_mouse(x, y) -> None:
    """Click the mouse at the current position or specified coordinates."""
    try:
        if x is not None and y is not None:
            pyautogui.click(x, y)
        else:
            pyautogui.click()
            return "mouse clicked"
    except Exception as e:
        return str(e)
    
def type_text(text) -> None:
    """Type the specified text."""
    try:
        pyautogui.typewrite(text)
        return "text typed"
    except Exception as e:
        return str(e)
    
def press_key(key) -> None:
    """Press the specified key."""
    try:
        pyautogui.press(key)
        return "key pressed"
    except Exception as e:
        return str(e)
    
def take_screenshot(filename=None):
    """Take a screenshot of the entire screen."""
    try:
        if filename is None:
            filename = "screenshot.png"

        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot/" + filename)

        return f"screenshot taken, file name: {filename}"
    except Exception as e:
        return str(e)


# Example usage
if __name__ == "__main__":
    move_mouse(100, 100)
    click_mouse()
    type_text("Hello, JARVIS!")
    press_key('enter')
    take_screenshot()
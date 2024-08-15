from modules.system import Environment

def _enable_speech(val):
    Environment.should_speak = val

def _enable_function_call(val):
    Environment.should_function_call = val

def toggle_settings(*args, **kwargs):
    Environment.default_working_directory = kwargs["default_working_directory"]
    Environment.curr_path = kwargs["curr_path"]
    Environment.verbose = kwargs["verbose"]
    Environment.should_speak = kwargs["should_speak"]
    Environment.should_function_call = kwargs["should_function_call"]
    Environment.screenshot_path = kwargs["screenshot_path"]
    return f"Settings updated to {kwargs}"

    

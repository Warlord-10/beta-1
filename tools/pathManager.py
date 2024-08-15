from modules.system import Environment
import os

def get_current_path():
    return Environment.curr_path

def set_current_path(path):
    Environment.setCurrentPath(path)
    return "Current Working Directory path set"

def move_into_subdirectory(subdirectory_name):
    new_path = os.path.join(Environment.curr_path, subdirectory_name)
    if os.path.isdir(new_path):
        Environment.setCurrentPath(new_path)
        print(f"Moved into subdirectory: {new_path}")
    else:
        print(f"Subdirectory {subdirectory_name} does not exist.")
    return "Moved into subdirectory"

def move_up_directory():
    new_path = os.path.dirname(Environment.curr_path)
    Environment.setCurrentPath(new_path)
    print(f"Moved up to directory: {new_path}")
    return "Moved up to directory"
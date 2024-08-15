import os
import shutil
import modules.system as system
from modules.system import Environment as _system_



def create_file(file_path, data=None):
    try:
        # if just file name is given then store in the cwd
        if os.path.basename(file_path) == file_path:
            file_path = os.path.join(_system_.getCurrentPath(), file_path)

        file = open(file_path, 'w', encoding='utf-8')
        if data is not None:
            file.write(data)
        file.close()
        return f"File created."
    except Exception as e:
        return str(e)
    
def write_file(file_path, content):
    try:
        if os.path.basename(file_path) == file_path:
            file_path = os.path.join(_system_.getCurrentPath(), file_path)
            
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"File written."
    except Exception as e:
        return str(e)
    
def update_file(file_path, content, position=None):
    try:
        if os.path.basename(file_path) == file_path:
            file_path = os.path.join(_system_.getCurrentPath(), file_path)

        if position is None:
            with open(file_path, 'a') as file:
                file.write(content)
        else:
            with open(file_path, 'r+') as file:
                file.seek(position)
                file.write(content)

        return f"File updated"
    except Exception as e:
        return str(e)

def upload_file(file_path):
    pass

def delete_file(file_path):
    try:
        if os.path.basename(file_path) == file_path:
            file_path = os.path.join(_system_.getCurrentPath(), file_path)

        os.remove(file_path)
        return f"File deleted."
    except Exception as e:
        return str(e)
    
def copy_file(src, dest):
    try:
        if os.path.basename(src) == src:
            src = os.path.join(_system_.getCurrentPath(), src)

        shutil.copy(src, dest)
        return f"File copied."
    except Exception as e:
        return str(e)
    
def list_files_and_folders(path=None):
    try:
        if path is None:
            path = _system_.getCurrentPath()

        return str(os.listdir(path))
    except Exception as e:
        return str(e)
    
def create_folder(folder_path):
    try:
        if os.path.basename(folder_path) == folder_path:
            folder_path = os.path.join(_system_.getCurrentPath(), folder_path)

        os.makedirs(folder_path, exist_ok=True)
        return "Folder created."
    except Exception as e:
        return str(e)
    
def delete_folder(folder_path):
    try:
        if os.path.basename(folder_path) == folder_path:
            folder_path = os.path.join(_system_.getCurrentPath(), folder_path)

        shutil.rmtree(folder_path)
        return "Folder deleted."
    except Exception as e:
        return str(e)


FILE_MANAGER_FUNC_MAP = {
    "create_file": create_file,
    "write_file": write_file,
    "update_file": update_file,
    "delete_file": delete_file,
    "copy_file": copy_file,
    "list_files_and_folders": list_files_and_folders,
    "create_folde": create_folder,
    "delete_folder": delete_folder
}
# Holds all the function declaration used for function calling
FILE_MANAGER_FUNC_DECL = [
    {
        "name": "create_file",
        "description": "Creates a file at the specified path. If data is provided, it will be written to the file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to create"
                },
                "data": {
                    "type": "string",
                    "description": "The data to write to the file (optional)"
                }
            },
            "required": [
                "file_path"
            ]
        }
    },
    {
        "name": "write_file",
        "description": "Writes content to a file at the specified path, overwriting any existing content.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write to"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file"
                }
            },
            "required": [
                "file_path",
                "content"
            ]
        }
    },
    {
        "name": "update_file",
        "description": "Updates a file at the specified path by writing content to it. Optionally, a position can be specified to write at a specific location in the file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                "type": "string",
                "description": "The path to the file to update"
                },
                "content": {
                "type": "string",
                "description": "The content to write to the file"
                },
                "position": {
                "type": "integer",
                "description": "The position in the file to write to (optional)"
                }
            },
            "required": [
                "file_path",
                "content"
            ]
        }
    },
    {
        "name": "delete_file",
        "description": "Deletes the file at the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                "type": "string",
                "description": "The path to the file to delete"
                }
            },
            "required": [
                "file_path"
            ]
        }
    },
    {
        "name": "copy_file",
        "description": "Copies a file from the source path to the destination path.",
        "parameters": {
            "type": "object",
            "properties": {
                "src": {
                "type": "string",
                "description": "The path to the source file"
                },
                "dest": {
                "type": "string",
                "description": "The path to the destination file"
                }
            },
            "required": [
                "src",
                "dest"
            ]
        }
    },
    {
        "name": "list_files_and_folders",
        "description": "Lists all files and folders in the specified directory. If the path is not provided, the current working directory will be used.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                "type": "string",
                "description": "The path to the directory to list"
                }
            }
        }
    },
    {
        "name": "create_folder",
        "description": "Creates a folder at the specified path. If the folder already exists, it will not be overwritten.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                "type": "string",
                "description": "The path to the folder to create"
                }
            },
            "required": [
                "folder_path"
            ]
        }
    },
    {
        "name": "delete_folder",
        "description": "Deletes the folder at the specified path, including all its contents.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "The path to the folder to delete"
                }
            },
            "required": [
                "folder_path"
            ]
        }
    }
]

OPERATIONS_FUNC_DECL = [
    {
        "name": "take_screenshot",
        "description": "Take a screenshot of the entire screen and save it as a PNG file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to save the screenshot as (including the .png extension). If not provided, defaults to 'screenshot.png'.",
                }
            }
        }
    }
]

LLM_FUNC_DECL = [
    {
        "name": "sendPrompt",
        "description": "Sends a message to the chat model, optionally including an image. Used only to gather extra information automatically",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The text message to send.",
                },
                "image_path": {
                    "type": "string",
                    "description": "The path to an image file to include with the message. (Optional, defaults to null)",
                }
            },
            "required":[
                "message"
            ]
        }
    }
]





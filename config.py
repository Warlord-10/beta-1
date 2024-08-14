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
    # {
    #     "name": "take_screenshot",
    #     "description": "Take a screenshot of the entire screen and save it as a PNG file.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "filename": {
    #                 "type": "string",
    #                 "description": "The name of the file to save the screenshot as (including the .png extension). If not provided, defaults to 'screenshot.png'.",
    #             }
    #         }
    #     }
    # }
]

LLM_FUNC_DECL = [
    # {
    #     "name": "send_information_to_LLM",
    #     "description": "Sends a prompt to the main LLM for processing.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "prompt": {
    #             "type": "string",
    #             "description": "The prompt to send to the LLM."
    #             }
    #         },
    #         "required": [
    #             "prompt"
    #         ]
    #     }
    # },
    {
        "name": "analyze_screen",
        "description": "Takes a screenshot and sends it to the main LLM for analysis."
    }
]

MEMORY_FUNC_DECL = [
    {
        "name": "saveTextToMemory",
        "description": "Saves the text into LLM's Memory(Brain).",
        "parameters": {
        "type": "object",
        "properties": {
            "text": {
            "type": "string",
            "description": "The text string to insert."
            }
        },
        "required": [
            "text"
        ]
        }
    },
    {
        "name": "saveDocumentToMemory",
        "description": "Saves a document into the LLM's Memory(Brain).",
        "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
            "type": "string",
            "description": "The path to the document file."
            }
        },
        "required": [
            "file_path"
        ]
        }
    },
    {
        "name": "clearMemory",
        "description": "Forgets everything, thus empties the Memory."
    },
    {
        "name": "queryMemory",
        "description": "Fetches data from the Memory.",
        "parameters": {
        "type": "object",
        "properties": {
            "query": {
            "type": "string",
            "description": "The query string to use for retrieval."
            }
        },
        "required": [
            "query"
        ]
        }
    }
]

BROWSER_FUNC_DECL = [
    {
        "name": "open_browser",
        "description": "Opens a web browser and performs a Google search using the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
            "search_query": {
                "type": "string",
                "description": "The search query to be used for the Google search."
            }
            },
            "required": [
            "search_query"
            ]
        }
    },
    {
        "name": "get_search_result",
        "description": "Retrieves Google search results for the given query and returns a dictionary of titles and corresponding URLs.",
        "parameters": {
            "type": "object",
            "properties": {
            "query": {
                "type": "string",
                "description": "The query string to use for retrieval of search results."
            }
            },
            "required": [
            "query"
            ]
        }
    }
]




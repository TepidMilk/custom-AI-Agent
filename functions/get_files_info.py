import os.path
import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    res = []
    abs_working = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(working_directory, directory))

    # check if the given path is relative to the working_directory so the AI agent doesn't work outside our working_directory
    if not os.path.exists(path):
        return f'Error: path to "{directory}" does not exist'
    if not path.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    
    # For each file in our directory we want to return data on it.
    files = os.listdir(path)
    for file in files:
        path_to_file = "/".join([path, file])
        file_string = f'- {file}: file_size={os.path.getsize(path_to_file)} bytes, is_dir={os.path.isdir(path_to_file)}'
        res.append(file_string)
    return "\n".join(res)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
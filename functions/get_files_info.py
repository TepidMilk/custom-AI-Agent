import os.path
import os

def get_files_info(working_directory, directory="."):
    full_directory = os.path.join(working_directory, directory)
    path = os.path.abspath(full_directory)
    if not os.path.exists(path):
        return f'Error: path to "{directory}" does not exist'
    if not path.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    with open(path, "r") as f:
        print(f)
    
    



get_files_info(os.getcwd(), "functions")
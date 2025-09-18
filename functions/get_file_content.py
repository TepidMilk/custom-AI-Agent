import subprocess, sys, os.path
from google.genai import types

MAX_LENGTH = 10000

def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(working_directory, file_path))

    #Check if file path is in working directory
    if not os.path.exists(path):
        return f'Error: Path to "{file_path}" does not exist'
    if not path.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(path, "r") as f:
        file_string = f.read(MAX_LENGTH)
        if os.path.getsize(path) > MAX_LENGTH:
            file_string += (
                f'[...File "{file_path}" truncated at {MAX_LENGTH} characters]'
            )
    return file_string

def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(working_directory, file_path))

    #check if file path is in working directory
    if not path.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        with open(path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing to file "{file_path}": {e}'
    
def run_python_file(working_directory, file_path, args=[]):
    res = []
    abs_working = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(working_directory, file_path))

    if not path.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    if not path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(args=([sys.executable, path] + args), timeout=30, capture_output=True, cwd=abs_working, check=True)
        res.append(f'STDOUT: {completed_process.stdout}')
        res.append(f'STDERR: {completed_process.stderr}')

        return "\n".join(res)
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="overwrite or create a file with specified content at a specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to or create, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be used to create or overwrite at the given file path."
            )
        },
        required=["file_path", "content"]
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="return up to 10000 characters of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="return the STDOUT and STDERR of subprocess.run on a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="arguments to be passed in to the executed python file."
            )
        },
    ),
)
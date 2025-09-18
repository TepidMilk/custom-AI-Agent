import os, sys, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content, schema_write_file, schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Set a 'tone' for how the Ai should respond through this system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

#List of availble functions that the AI has access to 
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

# this will be called to start the AI Agent
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('user_prompt') 
    parser.add_argument('-v', '--verbose', action='store_true', help="show token usage and response roles")
    args = parser.parse_args()

    #We want to keep track of an ongoing conversation with the AI Agent so the messages are a list
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))
    p_tokens = response.usage_metadata.prompt_token_count
    r_tokens = response.usage_metadata.candidates_token_count

    #if verbose is true we want to show the user the prompt as well as their tokens used. We always want to show the response
    if args.verbose:     
        print(f'\nUser prompt: {args.user_prompt}\n')
        print(f'Prompt tokens: {p_tokens}')
        print(f'Response tokens: {r_tokens}\n')

    #print out what functions the AI calls to use so we can run them
    if not response.function_calls == None:
        for f in response.function_calls:
            print(f'Calling function: {f.name}({f.args})')
    else:
        print(response.text)

if __name__ == "__main__":
    main()

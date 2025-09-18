import os, sys, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, schema_write_file, schema_run_python_file, get_file_content, write_file, run_python_file


# Set a 'tone' for how the Ai should respond through this system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

#Dictionary of functions to be called by the ai by name
FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}


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
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument('user_prompt') 
    parser.add_argument('-v', '--verbose', action='store_true', help="show token usage and response roles")
    args = parser.parse_args()

    #if verbose is true we want to show the user the prompt as well as their tokens used. We always want to show the response
    if args.verbose:     
        print(f'\nUser prompt: {args.user_prompt}\n')

    #We want to keep track of an ongoing conversation with the AI Agent so the messages are a list
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    for i in range(20):
        try:
            response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))
            
            if args.verbose:
                print("Prompt Tokens:", response.usage_metadata.prompt_token_count)
                print("Response Tokens:", response.usage_metadata.candidates_token_count)

            if response.candidates:
                for candidate in response.candidates:
                    function_call_content = candidate.content
                    messages.append(function_call_content)
    
            #print out what functions the AI calls to use so we can run them
            function_responses = []
            if not response.function_calls == None:
                for f in response.function_calls:
                    content = call_function(f, args.verbose)
                    if content.parts[0].function_response.response == None:
                        raise ValueError("Error: response is none")
                    elif args.verbose:
                        print(f"-> {content.parts[0].function_response.response['result']}")
                    function_responses.append(content.parts[0])
                messages.append(types.Content(role="user", parts=function_responses))
            else:
                print(response.text)
                break
        except Exception as e:
            print(f'Error: {e}')

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f'Calling function: {function_call_part.name}({function_call_part.args})')
    else:
        print(f' - Calling function: {function_call_part.name}')

    if function_call_part.name not in FUNCTIONS:
        return types.Content(
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    function_call_part.args["working_directory"] = "./calculator"
    res = FUNCTIONS[function_call_part.name](**function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": res},
            )
        ],
    )

if __name__ == "__main__":
    main()

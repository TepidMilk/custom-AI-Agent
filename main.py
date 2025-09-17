import os, sys, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

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

    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
    p_tokens = response.usage_metadata.prompt_token_count
    r_tokens = response.usage_metadata.candidates_token_count

    #if verbose is true we want to show the user the prompt as well as their tokens used. We always want to show the response
    if args.verbose:     
        print(f'\nUser prompt: {args.user_prompt}\n')
        print(f'Prompt tokens: {p_tokens}')
        print(f'Response tokens: {r_tokens}\n')
    print(response.text)

if __name__ == "__main__":
    main()

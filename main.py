"""
main.py
"""

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import SYSTEM_PROMPT
from functions.call_function import AVAILABLE_FUNC, call_function


def print_verbose(
        args_list:list[str],
        response:types.GenerateContentResponse
        ) -> None:
    """
    Print information about the response
    """
    print(f"User prompt: {args_list[1]}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_llm(
        llm_client: genai.Client,
        msgs: list[str],
        args: list[str],
        verbose: bool
        ) -> types.GenerateContentResponse:
    """
    Calls the LLM
    """
    for _ in range(20):

        # Call the API
        try:
            response = llm_client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=msgs,
                config=types.GenerateContentConfig(
                    tools=[AVAILABLE_FUNC],
                    system_instruction=SYSTEM_PROMPT
                )
            )
        except Exception as err:
            error_msg = types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name="llm_client.models.generate_content",
                        response={"error": f"Error occured while performing: llm_client.models.generate_content: {err}"},
                    )
                ],
            )
            msgs.append(error_msg)
            continue

        # Check for the response
        if response.text:
            # Print the response
            print(f"Response: {response.text}")

            if verbose:
                print_verbose(args, response)
            return

        # Check for candidates and append its content to messages
        for candidate in response.candidates:
            msgs.append(candidate.content)

        # Call the function the LLM has chosen
        if response.function_calls:
            for function in response.function_calls:
                msgs.append(call_function(function, verbose))

    # If the loop ends without response, raise an Error
    raise RuntimeError("The LLM was not able to find an answer after 20 iterations ...")


def main(args):
    """
    Main function
    """
    if len(args) == 1:
        raise ValueError("Brother, you have to provide the prompt")

    # Verbose bool
    verbose = "--verbose" in args

    # Load API Key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # Create Gemini-client instance
    gem_client = genai.Client(api_key=api_key)

    # Create list of messages
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args[1])]
        )
    ]

    # Call the LLM
    call_llm(gem_client, messages, args, verbose)


if __name__ == "__main__":
    main(sys.argv)

"""
call_function.py
"""

from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

# Dict mapping function names with the function itself
FUNC_NAME_TO_FUNC = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

# List of Available functions for the LLM to call
AVAILABLE_FUNC = types.Tool(
        function_declarations=[
            schema_get_file_content,
            schema_get_files_info,
            schema_run_python_file,
            schema_write_file
        ]
    )


def call_function(
        f:types.FunctionCall,
        verbose:bool =False
        ):
    """
    Calls the function specified in 'f' variable
    If verbose is specifies prints the function name and args.
    
    Params:
        - f: types.FunctionCall object to call.
        - verbose: bool Optional argument to indicate wheter the funtion's
            name and args are printed.
    """

    # Get funtion's name and args
    f_name = f.name
    f_args = f.args

    # Add working directory to f_args dict
    f_args["w_dir"] = "./calculator"

    if verbose:
        print(f"Calling function: {f_name}({f_args})")

    else:
        print(f" - Calling function: {f_name}")

    # Check the name is present on available functions
    if f_name not in FUNC_NAME_TO_FUNC.keys():
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=f_name,
                    response={"error": f"Unknown function: {f_name}"},
                )
            ],
        )

    # Call the function
    try:
        f_result = FUNC_NAME_TO_FUNC[f_name](**f_args)

    except Exception as err:
        f_result = f"Error: While calling function {f_name} error occurred: {err}"

    # Return the result as types.Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=f_name,
                response={"result": f_result},
            )
        ],
    )

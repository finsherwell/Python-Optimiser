import argparse as ap
import cProfile
import pstats
import io
import ast

from pathlib import Path

def get_user_defined_functions(target_script):
    # Get the file path of target script
    file_path = Path(target_script)

    # Check passed file path is a file
    if not file_path.is_file():
        print(f"Error: The file '{target_script}' does not exist.")
        return

    # Read the file
    with open (file_path, 'r') as file:
        # Parse file contents to an ast
        tree = ast.parse(file.read())
    
        # Return a list of function names (sync and async)
        return [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]

def profile_script(target_script):
    # Get names of all user defined functions
    funcs_to_show = get_user_defined_functions(target_script)

    # Ensure target script exists
    if not Path(target_script).is_file():
        print(f"Error: The file '{target_script}' does not exist.")
        return
    
    print(f"The profiler is profiling the script: {target_script}")

    # Use cProfile to run target script
    profiler = cProfile.Profile()
    profiler.enable()

    # Execute the target script
    try:
        with open(target_script, 'r') as file:
            script_code = file.read()
            exec(script_code, {'__name__': '__main__'})  # Execute script in the current namespace
    except Exception as e:
        print(f"Error: Failed to execute {target_script}. {e}")
        return
    finally:
        profiler.disable()

    # Process and display profiling results
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)

    # Show top 10 slowest functions
    stats.strip_dirs().sort_stats('cumulative')

    for func in funcs_to_show:
        stats.print_stats(func)

    # Show results
    print("\nProfiling Results:")
    print(stream.getvalue())


def main():
    parser = ap.ArgumentParser(description="Profile a Python script.")
    parser.add_argument('script', help="The path to the Python script to profile.")
    args = parser.parse_args()

    profile_script(args.script)

if __name__ == "__main__":
    main()
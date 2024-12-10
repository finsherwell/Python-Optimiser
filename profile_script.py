import cProfile
import pstats
import io
import ast
import json
import hashlib

from pathlib import Path

def get_function_hash(file_name, func_name, cumtime):
    """
    Generate a unique hash for each function's profiling data (based on file, function name and cumtime).
    Can detect changes in function due to changes in hash from change in cumtime.
    """
    return hashlib.sha256(f"{file_name}_{func_name}_{cumtime}".encode()).hexdigest()

def read_cache(cache_file):
    """
    Read the cache file and return the stored data as a dictionary, otherwise returns an empty dictionary.
    """
    if not Path(cache_file).is_file():
        with open(cache_file, "r") as file:
            return json.load(file)
    return {}

def write_cache(cache_file, cache_data):
    """
    Write the cache data to a JSON file.
    """
    sorted_cache_data = dict(sorted(cache_data.items(), key=lambda item: item[1]["hash"]))
    with open(cache_file, "w") as f:
        json.dump(sorted_cache_data, f, indent=4)

def get_user_defined_functions(target_script):
    """
    Gets all the user defined functions in the specified script by using an ast
    """
    file_path = Path(target_script)

    with open (file_path, 'r') as file:
        tree = ast.parse(file.read())
        return [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]

def update_profile_values(profile_data, keys_to_find):
    """
    Iterate through the profile data and assign values to the keys_to_find dictionary
    based on the matching function names in the profile data.
    
    :param profile_data: The profiling data, a dictionary of function profiles.
    :param keys_to_find: A dictionary where the keys are function names we want to find,
                          and values are initially empty (e.g., None or any placeholder).
    :return: The updated dictionary with values filled for matched keys.
    """
    
    # Iterate through the profile data and keys_to_find
    for func_name, profile in profile_data:
        if func_name in keys_to_find:
            # Assign the profile data to the dictionary key
            keys_to_find[func_name] = {
                "ncalls": profile.ncalls,
                "tottime": profile.tottime,
                "cumtime": profile.cumtime,
                "percall_tottime": profile.percall_tottime,
                "percall_cumtime": profile.percall_cumtime
            }
        
        # If all keys are found, break out of the loop
        if all(value is not None for value in keys_to_find.values()):
            break

    return keys_to_find

def profile_script(target_script, cache_file="profiling_cache.json"):
    # Ensure target script exists
    if not Path(target_script).is_file():
        print(f"Error: The file '{target_script}' does not exist.")
        return

        # Get names of all user defined functions
    funcs_to_show = get_user_defined_functions(target_script)
    
    print(f"The profiler is profiling the script: {target_script}")

    profiler = cProfile.Profile()
    profiler.enable()

    try:
        with open(target_script, 'r') as file:
            script_code = file.read()
            exec(script_code, {'__name__': '__main__'})
    except Exception as e:
        print(f"Error: Failed to execute {target_script}. {e}")
        return
    finally:
        profiler.disable()

    # Read the existing cache data
    cache_data = read_cache(cache_file)

    # Process the profiling results
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs().sort_stats('cumulative')
    # Example of filtering out irrelevant function profiles

    print(update_profile_values(stats.get_stats_profile, funcs_to_show))

    """
    new_cache = {}  # To store the new cache data


    # Write the updated cache if there are new or changed functions
    if new_cache:
        cache_data.update(new_cache)
        write_cache(cache_file, cache_data)
        print("Profiling results updated in cache.")
    else:
        print("No changes detected. Cache is up-to-date.")
    """

def main():
    target_script = "test_script.py"
    profile_script(target_script)

if __name__ == "__main__":
    main()
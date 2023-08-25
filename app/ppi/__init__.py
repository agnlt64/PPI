import ast
import os
import glob
import time

from PyLog.logger import Logger
from .levenshtein import lev
from .normalize import normalize, get_normalized_args, get_signature, get_function_name, remove_args
from .utils import read_json_file, read_source_file, save_json, JSON_OUTPUT

# Type alias to represent a function.
# Looks like this:
# function = {
#     'name': 'randint',
#     'args': ['a', 'b'],
#     'nb_args': 2
#     'filename': 'random.py',
#     'line': '12'
# }
FunctionType = dict[str, list[str], str, str]

STDLIB_IGNORE = ['test', 'site-packages', 'lib2to3']

logger = Logger()


def get_function_from_node(node: ast.AST, file_path: os.PathLike, abspath: bool = False) -> FunctionType:
    """
    Returns a `FunctionType` object from an `ast.AST` node.
    """
    name = node.name
    args = node.args.args
    new_function = {
        'name': name,
        'args': [arg.arg for arg in args],
        'nb_args': len(args),
        'filename': file_path if not abspath else os.path.abspath(file_path),
        'line': node.lineno,
    }
    return new_function


def index_folder(base_folder: os.PathLike, folders_to_ignore: list[str] = [], output: str = JSON_OUTPUT, web_context: bool = False) -> list[FunctionType]:
    """
    Index the `base_folder` while ignoring the `folder_to_ignore` list. See `STDLIB_IGNORE` for the defaults folders that will be ignored.
    When the indexing is done, the functions that have been parsed are saved to the `JSON_OUTPUT` file by default.
    If the file already exists when the function is called, the `base_folder` is not indexed and the content of the file is returned.
    """
    # before indexing, check if there is the JSON file functions.json
    if not web_context:
        logger.warning(f'Not indexing {base_folder}, reading the content of {output}. If you want to avoid this behaviour, either delete or rename {JSON_OUTPUT}.')
        if os.path.exists(output):
            return read_json_file(output)

    functions = []
    folders_to_ignore += STDLIB_IGNORE
    start = time.time()
    for filename in glob.iglob(f'{base_folder}/**', recursive=True):
        current_dir = filename.split('/')
        # https://stackoverflow.com/questions/3170055/test-if-lists-share-any-items-in-python (for 👇)
        want_to_continue = filename.endswith('py') and not bool(set(current_dir) & set(folders_to_ignore))
        if os.path.isfile(filename) and want_to_continue:
            if not web_context:
                logger.info(f'Reading {filename}...')
            source_code = read_source_file(filename)
            if not web_context:
                logger.info(f'Parsing {filename}...')
            parsed = ast.parse(source_code)
            # go through the AST
            for node in ast.walk(parsed):
                # no constructors
                if isinstance(node, ast.FunctionDef) and not node.name.startswith('__'):
                    new_function = get_function_from_node(node, filename)
                    functions.append(new_function)
    # save the results to a JSON file
    logger.info(f'Saving the results to {output}...')
    save_json(content=functions, filename=output)
    end = time.time()
    logger.info(f'Indexed folder {base_folder} in {end - start} seconds.')
    print(logger.RESET)
    return functions


def sort(query: str, functions: list[FunctionType]) -> list:
    """
    Sort the functions using the `levenshtein.lev()` function.
    """
    sorted_functions = []
    for f in functions:
        normalized = normalize(query)
        args = get_normalized_args(normalized)
        f_signature = normalize(get_signature(f))
        if args == '*':
            query_name = get_function_name(query)
            name = get_function_name(f_signature)
            sorted_functions.append((lev(query_name, name), f))
        elif '_' in args and len(args.split(', ')) == f['nb_args']:
            strip_query = query.replace(args, '')
            sorted_functions.append((lev(strip_query, remove_args(f_signature)), f))
        else:
            sorted_functions.append((lev(query, f_signature), f))
    return sorted(sorted_functions, key=lambda x: x[0])


# query = normalize('is zipfile(_)')
# print(get_normalized_args(query))
# functions = sort(query, index_folder('./stdlib'))
# print(get_signature(functions[i][1], True))

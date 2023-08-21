import ast
import typing
import os
import glob
import time
import json
from PyLog.logger import Logger

FunctionType = dict[str, tuple[str, str | typing.Any]]
JSON_OUTPUT = 'functions.json'
logger = Logger(log_to_file=True)

def read_source_file(filename: os.PathLike) -> str:
    with open(filename, 'r') as source:
        return source.read()


def save_json(content: dict, filename: str = JSON_OUTPUT) -> None:
    data = json.dumps(content, indent=4)
    with open(filename, 'w') as out:
        print(data, file=out)
        
def read_json_file(filename: str = JSON_OUTPUT):
    with open(filename) as f:
        return json.load(f)
        

def print_func(function: dict, return_value: bool = False) -> str | None:
    args = ''
    for a in function['args']:
        args += str(a) + ', '
    signature = f"{function['filename']}:{function['line']} {function['name']}({args[:-2]})"
    return signature if return_value else print(signature)


def get_function_from_node(node: ast.AST, file_path: os.PathLike, abspath: bool = False) -> FunctionType:
    name = node.name
    args = node.args.args
    new_function = {
        'name': name,
        'args': [arg.arg for arg in args],
        'filename': file_path if not abspath else os.path.abspath(file_path),
        'line': node.lineno,
        'col': node.col_offset
    }
    return new_function


def index_folder(base_folder: os.PathLike, folders_to_ignore: list[str] = ['test', 'site-packages', 'lib2to3']) -> list[FunctionType]:
    # before indexing, check if there is the JSON file functions.json
    logger.warning(f'Not indexing {base_folder}, reading the content of {JSON_OUTPUT}. If you want to avoid this behaviour, either delete or rename {JSON_OUTPUT}.')
    if os.path.exists(JSON_OUTPUT):
        return read_json_file(JSON_OUTPUT)
    
    functions = []
    start = time.time()
    for filename in glob.iglob(f'{base_folder}/**', recursive=True):
        current_dir = filename.split('/')
        # https://stackoverflow.com/questions/3170055/test-if-lists-share-any-items-in-python (for 👇)
        want_to_continue = filename.endswith('py') and not bool(set(current_dir) & set(folders_to_ignore))
        if os.path.isfile(filename) and want_to_continue:
            logger.info(f'Reading {filename}...')
            source_code = read_source_file(filename)
            logger.info(f'Parsing {filename}...')
            parsed = ast.parse(source_code)
            # go through the AST
            for node in ast.walk(parsed):
                # no constructors
                if isinstance(node, ast.FunctionDef) and not node.name.startswith('__'):
                    new_function = get_function_from_node(node, filename)
                    functions.append(new_function)
    # save the results to a JSON file
    logger.info(f'Saving the results to {JSON_OUTPUT}...')
    save_json(content=functions)
    end = time.time()
    logger.info(f'Indexed folder {base_folder} in {end - start} seconds.')
    return functions


functions = index_folder('./stdlib')
for i in range(10):
    print_func(functions[i])

import ast
import typing
import os
import glob
import time
import json
import random

from PyLog.logger import Logger
from levenshtein import lev

FunctionType = dict[str, tuple[str, str | typing.Any]]

STDLIB_IGNORE = ['test', 'site-packages', 'lib2to3']
JSON_OUTPUT = 'functions.json'

logger = Logger()

def read_source_file(filename: os.PathLike) -> str:
    with open(filename, 'r') as source:
        return source.read()


def save_json(content: list, filename: str = JSON_OUTPUT) -> None:
    data = json.dumps(content, indent=4)
    with open(filename, 'w') as out:
        print(data, file=out)


def read_json_file(filename: str = JSON_OUTPUT):
    with open(filename) as f:
        return json.load(f)
        

def get_signature(function: dict, file_infos: bool = False) -> str:
    args = ''
    for a in function['args']:
        args += str(a) + ', '
    signature = f"{function['name']}({args[:-2]})"
    if file_infos:
        signature = f"{function['filename']}:{function['line']} " + signature
    return signature



def get_function_from_node(node: ast.AST, file_path: os.PathLike, abspath: bool = False) -> FunctionType:
    name = node.name
    args = node.args.args
    new_function = {
        'name': name,
        'args': [arg.arg for arg in args],
        'filename': file_path if not abspath else os.path.abspath(file_path),
        'line': node.lineno,
    }
    return new_function


def normalize(query: str) -> str:
    split_query = query.split('(')
    name = split_query[0] # everything brefore the opening parenthesis
    name = '_'.join([a for a in name.split(' ') if a != ''])
    args = split_query[1].replace(')', '')
    args = ', '.join([a.lstrip().rstrip() for a in args.split(',')])
    return f'{name} ( {args} )'


def index_folder(base_folder: os.PathLike, folders_to_ignore: list[str] = []) -> list[FunctionType]:
    # before indexing, check if there is the JSON file functions.json
    logger.warning(f'Not indexing {base_folder}, reading the content of {JSON_OUTPUT}. If you want to avoid this behaviour, either delete or rename {JSON_OUTPUT}.')
    if os.path.exists(JSON_OUTPUT):
        return read_json_file(JSON_OUTPUT)
    
    functions = []
    folders_to_ignore += STDLIB_IGNORE
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

def sort(query: str, functions: list[FunctionType]) -> list:
    sorted_functions = []
    for f in functions:
        sorted_functions.append((lev(query, normalize(get_signature(f))), f))
    return sorted(sorted_functions, key=lambda x: x[0])

query = normalize('mainloop()')

functions = sort(query, index_folder('./stdlib'))

for i in range(10):
    print(get_signature(functions[i][1], True))

import os
import json

JSON_OUTPUT = 'functions.json'

def read_source_file(filename: os.PathLike) -> str:
    """
    Retrieves the content of the `filename`. Used to parse a Python file.
    """
    with open(filename, 'r', encoding='utf-8') as source:
        print(source)
        return source.read()


def save_json(content: list, filename: str = JSON_OUTPUT) -> None:
    """
    Save the `content` (Python dict) to the `filename`. By default, the filename is `JSON_OUTPUT`.
    """
    data = json.dumps(content, indent=4)
    with open(filename, 'w', encoding='utf-8') as out:
        out.write(data)


def read_json_file(filename: str = JSON_OUTPUT) -> dict:
    """
    Returns the content of the `filename` (must be a JSON file).
    """
    with open(filename, encoding='utf-8') as f:
        return json.load(f)
# Normalizer functions for the PPI Search Engine

from PyLog.logger import Logger

logger = Logger()

def _normalize(_query: str) -> tuple[str, str]:
    split_query = _query.split('(')
    name = split_query[0] # everything brefore the opening parenthesis
    name = '_'.join([a for a in name.split(' ') if a != ''])
    args = split_query[1].replace(')', '')
    args = ', '.join([a.lstrip().rstrip() for a in args.split(',')])
    return f'{name} ( {args} )', args

def normalize(query: str) -> str:
    """
    Universal format for a function signature and an user query.
    The format is `function_name_separated_with_underscored ( arg1, arg2, arg3 )`. 
    The number of spaces does not matter, which means that `is zipfile (filename)` and `is    zipfile ( filename)` 
    will both produce the same output, e. g `is_zipfile ( filename )`.
    """
    return _normalize(_query=query)[0]


def get_normalized_args(query: str) -> str:
    return _normalize(_query=query)[1]


def get_function_name(func) -> str:
    return func.split('(')[0].rstrip()


def remove_args(func: str) -> str:
    return func.replace(get_normalized_args(func), '')
    

# Tests
def test_func_normalizer() -> bool:
    test_cases = [
        ("random(a, b)", "random ( a, b )"),
        ("random (      a   ,     b   )", "random ( a, b )"),
        ("is zipfile(filename)", "is_zipfile ( filename )"),
    ]
    failed = False
    for i, (f, expected) in enumerate(test_cases):
        normalized_func = normalize(f)
        if normalized_func == expected:
            logger.info(f"Test {i + 1}: Passed ✅")
        else:
            logger.warning(f"Test case {i + 1}: Failed ❌. Expected {expected}, got {normalized_func}.")
            failed = True
    return failed

def test_args_normalizer() -> bool:
    test_cases = [
        ("random(a, b)", "a, b"),
        ("random (      a   ,     b   )", "a, b"),
        ("is zipfile(filename)", "filename"),
    ]
    failed = False
    for i, (f, expected) in enumerate(test_cases):
        normalized_args = get_normalized_args(f)
        if normalized_args == expected:
            logger.info(f"Test {i + 1}: Passed ✅")
        else:
            logger.warning(f"Test case {i + 1}: Failed ❌. Expected {expected}, got {normalized_args}.")
            failed = True
    return failed


def get_signature(function: dict, file_infos: bool = False) -> str:
    """
    Returns the function signature from a `function` dict.
    """
    args = ''
    for a in function['args']:
        args += str(a) + ', '
    signature = f"{function['name']}({args[:-2]})"
    if file_infos:
        # we put 2 spaces between the file path and the actual signature for easier JS parsing (do not change)
        signature = f"{function['filename']}:{function['line']}  " + signature
    return signature


if __name__ == '__main__':
    if test_func_normalizer() and test_args_normalizer():
        logger.info("All tests passed!")
    else:
        logger.error('Not all the tests have passed!')
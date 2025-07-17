# Python Project Indexer

This Python web application will index a specified folder (ignoring what you ask it to ignore) and will return a list of functions contained in the folder (aka Python project) matching the given signature, using the [Levenshtein](https://en.wikipedia.org/wiki/Levenshtein_distance) distance.

## Quick start
```console
git clone --recursive https://github.com/agnlt64/PPI.git
cd PPI
uv venv .venv
. .venv/bin/activate # Unix
.venv\Scripts\activate # Windows
uv sync
uv run main.py
```

## How to use it
Here is the syntax to make a query:
```
# if you know the name of the params
function_name(param1, param2, param3)
function name (param1, param2, param3)
# if you don't know the name of the params, but you know how many params the function accepts
function_name(_, _, _)
# if you know nothing but the name
function_name(*)
```
Note that the name does not have to be super accurate, the application will return the matching names according to the Levenshtein distance. The spacing is not important because all the inputs are formatted in the same way.

## Levenshtein distance tests
In the `levenshtein/__init__.py` file, there are some tests to confirm that the algorithm is implemented properly. See `levenshtein/big_ass_words.txt` for more details about the tested words.
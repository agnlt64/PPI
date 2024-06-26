# Python Project Indexer

This Python web application will index a specified folder (ignoring what you ask it to ignore) and will return a list of functions contained in the folder (aka Python project) matching the given signature, using the Levenshtein distance.

## Quick start
```console
git clone --recursive https://github.com/ABFStudio/PPI.git
cd PPI
python -m venv .env
. .env/bin/activate # Unix
.env\Scripts\Activate.ps1 # Windows
pip install -r requirements.txt
python main.py # start the webserver on 127.0.0.1:8080
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
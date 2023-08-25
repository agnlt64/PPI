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
Here is the sunyax to make a query:
```
function_name(param1, param2, param3)
```
Note that the function name does not need to be underscore-separated, it will be correctly formatted by the application. If you don't know the names of the parameters, you can use underscores: `function(_, _)`. The application will return all the functions that match the given name and the number of parameters.

## Levenshtein distance tests
In the `levenshtein/__init__.py` file, there are some tests to confirm that the algorithm is implemented properly. See `levenshtein/big_ass_words.txt` for more details about the tested words.
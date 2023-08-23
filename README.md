# Python Project Indexer

This Python web application will index a specified folder (ignoring what you ask it to ignore) and will return a list of functions contained in the folder (aka Python project) matching the given signature, using the Levenshtein distance.

## Quick start
```console
git clone --recursive https://github.com/ABFStudio/PPI.git
cd PPI
python main.py
```
Before running the script, make sure to change the folder you want to index at the bottom of `main.py`.

## Tests
In the `levenshtein.py` file, there are some tests to confirm that the algorithm is implemented properly. See `big_ass_words.txt` for more details about the tested words.
# Python Project Indexer

This Python script will index a project and return all the functions that match a specified signature/function name. It has no user interface at the moment, but this is planned. It uses the Levenshtein distance (see `levenshtein.py` for the implementation)

## Quick start
```console
git clone --recursive https://github.com/ABFStudio/PPI.git
cd PPI
python main.py
```
Before running the script, make sure to change the folder you want to index at the bottom of `main.py`.

## Tests
In the `levenshtein.py` file, there are some tests to confirm that the algorithm is implemented properly. See `big_ass_words.txt` for more details about the tested words.
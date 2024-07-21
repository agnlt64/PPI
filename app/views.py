from flask import Blueprint, render_template, request
import json

from .ppi import index_folder, sort, normalize, get_signature

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/search')
def search_folder():
    args = request.args.to_dict()
    folder = args['folder']
    folders_to_ignore = args.get('ignore').split() if args.get('ignore') is not None else [] # bruh mypy be dumb af
    numbers_of_functions = int(args['max'])
    signature = normalize(args['signature'])
    unsorted_functions = index_folder(folder, output='app/ppi/functions.json', web_context=True, folders_to_ignore=folders_to_ignore)
    sorted_functions = sort(signature, unsorted_functions)
    sorted_functions = [sorted_functions[i][1] for i in range(len(sorted_functions))]
    return json.dumps(sorted_functions[:numbers_of_functions])
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
    folder = args.get('folder')
    signature = normalize(args.get('signature'))
    unsorted_functions = index_folder(folder, output='app/ppi/functions.json', web_context=True)
    sorted_functions = sort(signature, unsorted_functions)
    functions = [get_signature(sorted_functions[i][1], file_infos=True) for i in range(len(sorted_functions))]
    return json.dumps(functions[:20])
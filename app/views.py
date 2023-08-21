from flask import Blueprint, render_template, redirect, request

from . import client_logger
from .ppi import index_folder, sort, normalize, get_signature

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/api/search', methods=['POST'])
def search_folder():
    args = request.args.to_dict()
    folder = args.get('folder')
    signature = normalize(args.get('signature'))
    functions = sort(signature, index_folder(folder, output='app/ppi/functions.json'))
    client_logger.info(functions[0][1])
    return redirect(request.referrer)
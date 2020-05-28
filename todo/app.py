import json
from flask import Flask, request, Response
from .storage import *

app = Flask(__name__)

storage = FileStorage()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/item/new', methods=['POST'])
def add_item():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']
    status = req_data.get('status')

    # Add item to the list
    res_data = storage.add_item(item, status)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error': 'Item not added - '}" + item, status=400,
                            mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response


@app.route('/items/all')
def get_all_items():
    # Get items from the storage
    res_data = storage.get_all_items()
    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response


@app.route('/item/status', methods=['GET'])
def get_item():
    # Get parameter from the URL
    item_id = request.args.get('item_id')

    # Get items from the storage
    status = storage.get_item(item_id)

    # Return 404 if item not found
    if status is None:
        response = Response("{'error': 'Item Not Found - '}" + item_id, status=404,
                            mimetype='application/json')
        return response

    # Return status
    res_data = {
        'status': status
    }

    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response


@app.route('/item/update', methods=['PUT'])
def update_status():
    # Get item from the POST body
    req_data = request.get_json()
    item_id = req_data['item_id']
    status = req_data['status']

    # Update item in the list
    res_data = storage.update_status(item_id, status)
    if res_data is None:
        response = Response("{'error': 'Error updating item - '" + item_id + ", " + status + "}",
                            status=400, mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response


@app.route('/item/remove', methods=['DELETE'])
def delete_item():
    # Get item from the POST body
    req_data = request.get_json()
    item_id = req_data['item_id']

    # Delete item from the list
    res_data = storage.delete_item(item_id)
    if res_data is None:
        response = Response("{'error': 'Error deleting item - '" + item_id + "}", status=400,
                            mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

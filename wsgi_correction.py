# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

import itertools

from flask import Flask, jsonify, abort, request
app = Flask(__name__)

BASE_URL = '/api/v1'
PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv' },
    3: { 'id': 3, 'name': 'Le Wagon'},
}
START_INDEX = len(PRODUCTS) + 1
IDENTIFIER_GENERATOR = itertools.count(START_INDEX)


@app.route(f'{BASE_URL}/products', methods=['GET'])
def read_many_products():
    products = list(PRODUCTS.values())

    return jsonify(products), 200


@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['GET'])
def read_one_product(product_id):
    if product_id not in PRODUCTS:
        abort(404)

    return jsonify(PRODUCTS[product_id]), 200


@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['DELETE'])
def delete_one_product(product_id):
    if product_id not in PRODUCTS:
        abort(404)
    else:
        del(PRODUCTS[product_id])

    return '', 204


@app.route(f'{BASE_URL}/products', methods=['POST'])
def create_one_product():
    data = request.get_json()

    if data is None or 'name' not in data:
        abort(400)

    if data['name'] == '' or not isinstance(data['name'], str):
        abort(422)

    next_id = next(IDENTIFIER_GENERATOR)
    PRODUCTS[next_id] = {'id' : next_id , 'name' : data['name'] }

    return jsonify(PRODUCTS[next_id]), 201


@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['PATCH'])
def update_one_product(product_id):
    data = request.get_json()

    if data is None or 'name' not in data:
        abort(400)

    if data['name'] == '' or not isinstance(data['name'], str):
        abort(422)

    if product_id not in PRODUCTS:
        abort(404)

    PRODUCTS[product_id]['name'] = data['name']

    return '', 204

# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, jsonify, abort, request
import itertools

app = Flask(__name__)

PRODUCTS = {
        1: { 'id': 1, 'name': 'Skello' },
        2: { 'id': 2, 'name': 'Socialive.tv' },
        3: { 'id': 3, 'name': 'Le Wagon'},
    }

START_INDEX = len(PRODUCTS) + 1

IDENTIFIER_GENERATOR = itertools.count(START_INDEX)

@app.route('/')
def hello():
    return "Hello World ! :) this is a test"

# READ
@app.route('/api/v1/products')
def get_products():
    #print('Hello I am in products method')
    return jsonify(PRODUCTS)

# READ
@app.route('/api/v1/products/<int:id>')
def get_product(id):
    # product does not exist => return 404 error code
    product = PRODUCTS.get(id)

    if product is None:
        abort(404)

    # product exists => return the product (JSON format)
    return jsonify(PRODUCTS[id]), 200

# DELETE
@app.route('/api/v1/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = PRODUCTS.pop(id, None)

    if product is None:
        abort(404)

    return '', 204

# CREATE
@app.route('/api/v1/products', methods=['POST'])
def create_product():
    new_product = request.get_json()

    if new_product is None:
        abort(404)

    name = new_product.get('name')

    if name == '':
        abort(422)

    next_id = next(IDENTIFIER_GENERATOR)

    PRODUCTS[next_id] = {'id': next_id, 'name': name}

    return jsonify(PRODUCTS[next_id]), 201

# UPDATE
@app.route('/api/v1/products/<int:id>', methods=['PATCH'])
def update_product(id):
    print(f'Existing PRODUCTS = {PRODUCTS}')
    data = request.get_json()
    new_name = data.get('name')

    print(f'Product {id} to update with new name {new_name}')

    if PRODUCTS.get(id) is None or new_name == '':
        print(f'Abort')
        abort(422)

    PRODUCTS[id]['name'] = new_name

    print(f'New PRODUCTS = {PRODUCTS}')
    return '', 204

if __name__ == "__main__":
    print(f'PRODUCTS = {PRODUCTS}')

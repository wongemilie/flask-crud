# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World ! :)"


@app.route('/api/v1/products')
def products():

    products = {
        1: { 'id': 1, 'name': 'Skello' },
        2: { 'id': 2, 'name': 'Socialive.tv' },
    }

    # products = {
    #     1: 'Skello',
    #     2: 'Socialive.tv',
    # }

    return jsonify(products)

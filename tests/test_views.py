# tests/test_views.py
from flask_testing import TestCase
from wsgi import app

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, dict)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.

    #  -- READ --
    def test_get_all_products(self):
        response = self.client.get("/api/v1/products")
        product = response.json
        status_code = response.status_code
        self.assertIsInstance(product, dict) # Check product is a JSON format
        self.assertTrue(product) # Check product is not empty
        self.assertEquals(status_code, 200) # Check request status code is 200

    def test_get_product_found(self):
        response = self.client.get("/api/v1/products/1")
        product = response.json
        status_code = response.status_code
        self.assertIsInstance(product, dict) # Check product is a JSON format
        self.assertIsNotNone(product) # Check product is not empty
        self.assertEquals(status_code, 200) # Check request status code is 200

    def test_get_product_not_found(self):
        response = self.client.get("/api/v1/products/1000")
        product = response.json
        status_code = response.status_code
        self.assertIsNone(product) # Check product is empty
        #self.assertFalse(product) # Check product is empty
        self.assertEquals(status_code, 404) # Check request status code is 404

    #  -- DELETE --
    def test_delete_product(self):
        response = self.client.delete("/api/v1/products/3")
        delete_result = response.json
        status_code = response.status_code
        self.assertIsNone(delete_result)
        self.assertEquals(status_code, 204) # Check request status code is 204

        # Check product does not exist anymore
        response = self.client.get("/api/v1/products/3")
        get_result = response.json
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(get_result)

    #  -- CREATE --
    def test_create_product(self):
        response = self.client.post("/api/v1/products", json={'name':'Netflix'})
        create_result = response.json
        status_code = response.status_code
        self.assertIsInstance(create_result, dict)
        self.assertIsNotNone(create_result)
        self.assertEquals(status_code, 201)

    #  -- UPDATE --
    def test_update_product_success(self):
        response = self.client.patch("/api/v1/products/2", json={'name':'Toto'})
        status_code = response.status_code
        self.assertEquals(status_code, 204)

    def test_update_product_id_not_found(self):
        response = self.client.patch("/api/v1/products/123", json={'name':'Hello'})
        status_code = response.status_code
        self.assertEquals(status_code, 422)

    def test_update_product_name_empty(self):
        response = self.client.patch("/api/v1/products/2", json={'name':''})
        status_code = response.status_code
        self.assertEquals(status_code, 422)

from odoo.tests.common import TransactionCase,tagged
from odoo.exceptions import ValidationError
import json


@tagged('material_unittest')
class TestMaterial(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestMaterial, self).setUp(*args, **kwargs)

        # Create a test supplier
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier A',
            'is_company': True,
            'supplier_rank': 2,
        })
        self.supplier_b = self.env['res.partner'].create({
            'name': 'Test Supplier B',
            'is_company': True,
            'supplier_rank': 3,
        })

        # Create some initial materials for testing
        self.material_fabric = self.env['material.material'].create({
            'material_code': 'FAB001',
            'material_name': 'Blue Denim Fabric',
            'material_type': 'fabric',
            'material_buy_price': 150.0,
            'supplier_id': self.supplier.id,
        })
        self.material_jeans = self.env['material.material'].create({
            'material_code': 'JNS001',
            'material_name': 'Black Jeans Material',
            'material_type': 'jeans',
            'material_buy_price': 200.0,
            'supplier_id': self.supplier_b.id,
        })

    def test_create_material_valid(self):
        """ Test creating a material with valid data. """
        new_material = self.env['material.material'].create({
            'material_code': 'COT001',
            'material_name': 'Pure Cotton',
            'material_type': 'cotton',
            'material_buy_price': 100.0,
            'supplier_id': self.supplier.id,
        })
        self.assertTrue(new_material.exists())
        self.assertEqual(new_material.material_code, 'COT001')
        self.assertEqual(new_material.material_buy_price, 100.0)

    def test_create_material_buy_price_too_low(self):
        """ Test creating a material with buy price less than 100. """
        with self.assertRaises(ValidationError):
            self.env['material.material'].create({
                'material_code': 'INV001',
                'material_name': 'Invalid Material',
                'material_type': 'fabric',
                'material_buy_price': 50.0,
                'supplier_id': self.supplier.id,
            })

    # def test_create_material_duplicate_code(self):
    #     """ Test creating a material with a duplicate material code. """
    #     with self.assertRaisesRegex(Exception, 'Material Code must be unique!'):
    #         self.env['material.material'].create({
    #             'material_code': 'FAB001', # Duplicate
    #             'material_name': 'Another Fabric',
    #             'material_type': 'fabric',
    #             'material_buy_price': 180.0,
    #             'supplier_id': self.supplier.id,
    #         })
            # Odoo 14 might raise this as a psycopg2.IntegrityError,
            # which is an Exception, and the regex will match the constraint message.

    def test_update_material_valid(self):
        """ Test updating an existing material. """
        self.material_fabric.write({
            'material_name': 'Updated Blue Denim',
            'material_buy_price': 170.0,
        })
        self.assertEqual(self.material_fabric.material_name, 'Updated Blue Denim')
        self.assertEqual(self.material_fabric.material_buy_price, 170.0)

    def test_update_material_buy_price_too_low(self):
        """ Test updating material with buy price less than 100. """
        with self.assertRaises(ValidationError):
            self.material_jeans.write({'material_buy_price': 99.0})

    def test_delete_material(self):
        """ Test deleting a material. """
        material_count_before = self.env['material.material'].search_count([])
        self.material_fabric.unlink()
        material_count_after = self.env['material.material'].search_count([])
        self.assertEqual(material_count_before - 1, material_count_after)
        self.assertFalse(self.material_fabric.exists())


    # # --- API Tests ---

    # def test_api_get_materials(self):
    #     """ Test GET /api/materials """
    #     url = '/api/materials'
    #     response = self.url_open(url)
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.text)
    #     self.assertIsInstance(data, list)
    #     self.assertGreaterEqual(len(data), 2) # At least our two initial materials

    #     # Test filter by type
    #     response_fabric = self.url_open(url + '?material_type=fabric')
    #     self.assertEqual(response_fabric.status_code, 200)
    #     data_fabric = json.loads(response_fabric.text)
    #     self.assertGreaterEqual(len(data_fabric), 1)
    #     for material in data_fabric:
    #         self.assertEqual(material['material_type'], 'fabric')

    # def test_api_post_material_valid(self):
    #     """ Test POST /api/materials with valid data. """
    #     url = '/api/materials'
    #     post_data = {
    #         'material_code': 'TEST001',
    #         'material_name': 'Test Fabric API',
    #         'material_type': 'fabric',
    #         'material_buy_price': 125.0,
    #         'supplier_id': self.supplier.id,
    #     }
    #     response = self.url_json(url, post_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('id', response.json())
    #     self.assertIn('message', response.json())
    #     self.assertEqual(response.json()['message'], 'Material created successfully!')

    #     # Verify creation
    #     created_material = self.env['material.material'].sudo().browse(response.json()['id'])
    #     self.assertTrue(created_material.exists())
    #     self.assertEqual(created_material.material_code, 'TEST001')

    # def test_api_post_material_invalid_buy_price(self):
    #     """ Test POST /api/materials with buy_price < 100. """
    #     url = '/api/materials'
    #     post_data = {
    #         'material_code': 'BAD001',
    #         'material_name': 'Bad Price',
    #         'material_type': 'cotton',
    #         'material_buy_price': 90.0, # Invalid
    #         'supplier_id': self.supplier.id,
    #     }
    #     response = self.url_json(url, post_data)
    #     self.assertEqual(response.status_code, 400) # Expecting bad request
    #     self.assertIn('error', response.json())
    #     self.assertIn('Material Buy Price cannot be less than 100.', response.json()['error'])

    # def test_api_post_material_duplicate_code(self):
    #     """ Test POST /api/materials with duplicate material_code. """
    #     url = '/api/materials'
    #     post_data = {
    #         'material_code': 'FAB001', # Duplicate of existing
    #         'material_name': 'Duplicate Test',
    #         'material_type': 'fabric',
    #         'material_buy_price': 110.0,
    #         'supplier_id': self.supplier.id,
    #     }
    #     response = self.url_json(url, post_data)
    #     self.assertEqual(response.status_code, 409) # Expecting Conflict
    #     self.assertIn('error', response.json())
    #     self.assertIn('Material Code must be unique!', response.json()['error'])


    # def test_api_put_material_valid(self):
    #     """ Test PUT /api/materials/<id> with valid data. """
    #     url = f'/api/materials/{self.material_fabric.id}'
    #     put_data = {
    #         'material_name': 'Updated Fabric API',
    #         'material_buy_price': 190.0,
    #     }
    #     response = self.url_json(url, put_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('message', response.json())
    #     self.assertEqual(response.json()['message'], 'Material updated successfully!')

    #     # Verify update
    #     self.material_fabric.invalidate_cache() # Clear cache to get fresh data
    #     self.assertEqual(self.material_fabric.material_name, 'Updated Fabric API')
    #     self.assertEqual(self.material_fabric.material_buy_price, 190.0)

    # def test_api_put_material_invalid_buy_price(self):
    #     """ Test PUT /api/materials/<id> with buy_price < 100. """
    #     url = f'/api/materials/{self.material_jeans.id}'
    #     put_data = {
    #         'material_buy_price': 80.0, # Invalid
    #     }
    #     response = self.url_json(url, put_data)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn('error', response.json())
    #     self.assertIn('Material Buy Price cannot be less than 100.', response.json()['error'])

    # def test_api_delete_material(self):
    #     """ Test DELETE /api/materials/<id>. """
    #     material_to_delete = self.env['material.material'].create({
    #         'material_code': 'DEL001',
    #         'material_name': 'Material to Delete',
    #         'material_type': 'cotton',
    #         'material_buy_price': 110.0,
    #         'supplier_id': self.supplier.id,
    #     })
    #     url = f'/api/materials/{material_to_delete.id}'
    #     response = self.url_open(url, method='DELETE')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('message', json.loads(response.text))
    #     self.assertEqual(json.loads(response.text)['message'], 'Material deleted successfully!')

    #     # Verify deletion
    #     self.assertFalse(material_to_delete.exists())

    # def test_api_delete_material_not_found(self):
    #     """ Test DELETE /api/materials/<id> for non-existent ID. """
    #     url = '/api/materials/999999' # Non-existent ID
    #     response = self.url_open(url, method='DELETE')
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn('error', json.loads(response.text))
    #     self.assertEqual(json.loads(response.text)['error'], 'Material not found.')
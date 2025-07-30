from odoo.tests.common import TransactionCase,tagged, HttpCase
from odoo.exceptions import ValidationError
import json
from urllib.request import Request

@tagged('material_unittest')
class TestMaterial(HttpCase):
    def setUp(self, *args, **kwargs):
        super(TestMaterial, self).setUp(*args, **kwargs)
        self.supplier = self.env['res.partner'].create({'name': 'Test Supplier for Material'})
        self.material_to_update = self.env['material.material'].create({
            'material_code': 'UPD001poo',
            'material_name': 'Original Material',
            'material_type': 'fabric',
            'material_buy_price': 125.0,
            'supplier_id': self.supplier.id,
        })
        self.material_jeans = self.env['material.material'].create({
            'material_code': 'JNS001x',
            'material_name': 'Jeans Material',
            'material_type': 'jeans',
            'material_buy_price': 150.0,
            'supplier_id': self.supplier.id,
        })
        self.api_base_url = "http://localhost:8069"

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
    def test_api_get_materials(self):
        """ Test GET /api/materials """
        url = '/api/materials'
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2) 

        # Test filter by type
        response_fabric = self.url_open(url + '?material_type=fabric')
        self.assertEqual(response_fabric.status_code, 200)
        data_fabric = json.loads(response_fabric.text)
        self.assertGreaterEqual(len(data_fabric), 1)
        for material in data_fabric:
            self.assertEqual(material['material_type'], 'fabric')

    def test_api_post_material_valid(self):
        """ Test POST /api/materials with valid data. """
        url = f'{self.api_base_url}/api/materials' 
        post_data = {
            'material_code': 'TEST001',
            'material_name': 'Test Fabric API',
            'material_type': 'fabric',
            'material_buy_price': 125.0,
            'supplier_id': self.supplier.id,
        }

        response = self.opener.post(url, json=post_data) 
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        
        self.assertIn('result', response_data)
        result_data = response_data['result']

        self.assertIn('id', result_data) 
        self.assertIn('message', result_data) 
        self.assertEqual(result_data['message'], 'Material created successfully!') 

        # Verify creation
        created_material = self.env['material.material'].sudo().browse(result_data['id']) 
        self.assertTrue(created_material.exists())
        self.assertEqual(created_material.material_code, 'TEST001')

    def test_api_post_material_invalid_buy_price(self):
        """ Test POST /api/materials with buy_price < 100. """
        url = f'{self.api_base_url}/api/materials' 
        post_data = {
            'material_code': 'BAD001',
            'material_name': 'Bad Price',
            'material_type': 'cotton',
            'material_buy_price': 90.0,
            'supplier_id': self.supplier.id,
        }
        
        response = self.opener.post(url, json=post_data) 

        response_data = response.json() 


        self.assertIn('result', response_data)
        result_content = response_data['result']
        self.assertEqual(result_content['status_code'], 400) 

        created_material = self.env['material.material'].sudo().search([('material_code', '=', 'BAD001')])
        self.assertFalse(created_material, "Material with invalid price should not have been created")
    
    def test_api_put_material_valid(self):
        """ Test PUT /api/materials/<id> with valid data. """
        updated_data = {
            'material_name': 'Original Material',
            'material_buy_price': 125.0,
            'material_type': 'cotton',
        }
        
        material_id = self.material_to_update.id

        url = f'{self.api_base_url}/api/materials/{material_id}' 

        response = self.opener.put(url, json=updated_data) 
    
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json() 
        
        self.assertIn('result', response_data)
        result_data = response_data['result']

        self.assertIn('message', result_data) 
        self.assertEqual(result_data['message'], 'Material updated successfully!')

    def test_api_put_material_invalid_buy_price(self):
        """ Test PUT /api/materials/<id> with buy_price < 100. """
        url = f'{self.api_base_url}/api/materials/{self.material_jeans.id}' 
        
        put_data = {
            'material_buy_price': 80.0,
        }
        
        response = self.opener.put(url, json=put_data) 
        response_data = response.json() 
        self.assertIn('result', response_data)

        result_content = response_data['result']
        self.assertEqual(result_content['status_code'], 400) 
        self.assertIn('Material Buy Price cannot be less than 100.', result_content['error'])

    def test_api_delete_material(self):
        """ Test DELETE /api/materials/<id>. """
        material_to_delete = self.env['material.material'].create({
            'material_code': 'DEL001',
            'material_name': 'Material to Delete',
            'material_type': 'cotton',
            'material_buy_price': 110.0,
            'supplier_id': self.supplier.id,
        })
        url = f'{self.api_base_url}/api/materials/{material_to_delete.id}'
        
        response = self.opener.delete(url) 

        self.assertEqual(response.status_code, 200)

    def test_api_delete_material_not_found(self):
        """ Test DELETE /api/materials/<id> for non-existent ID. """
        url = f'{self.api_base_url}/api/materials/999999' 
        
        response = self.opener.delete(url) 

        self.assertEqual(response.status_code, 404)
        
        response_data = response.json() 
        
        self.assertIn('error', response_data) 
        error_details = response_data['error']
        self.assertEqual(error_details, 'Material not found.')
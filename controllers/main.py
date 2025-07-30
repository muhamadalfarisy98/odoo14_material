import json
from odoo import http
from odoo.http import request,Response

class MaterialController(http.Controller):
    _name = '/api/materials'

    @http.route('/api/materials', type='http', auth='public', methods=['GET'], csrf=False)
    def get_materials(self, **kw):
        """
        API endpoint to retrieve all materials or filter by material_type.
        Example: GET /api/materials?material_type=fabric
        """
        try:
            domain = []
            material_type = kw.get('material_type')
            if material_type:
                # Validate material_type to prevent arbitrary string injection
                allowed_types = ['fabric', 'jeans', 'cotton']
                if material_type.lower() not in allowed_types:
                    return Response(
                        json.dumps({'error': 'Invalid material_type. Allowed types are: fabric, jeans, cotton.'}),
                        headers={'Content-Type': 'application/json'},
                        status=400
                    )
                domain.append(('material_type', '=', material_type.lower()))

            materials = request.env['material.material'].sudo().search(domain)
            material_data = []
            for material in materials:
                material_data.append({
                    'id': material.id,
                    'material_code': material.material_code,
                    'material_name': material.material_name,
                    'material_type': material.material_type,
                    'material_buy_price': material.material_buy_price,
                    'supplier_name': material.supplier_id.name,
                    'supplier_id': material.supplier_id.id,
                })
            return Response(
                json.dumps(material_data),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            return Response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=500
            )

    @http.route('/api/materials', type='json', auth='public', methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        """
        API endpoint to create a new material.
        Required fields: material_code, material_name, material_type, material_buy_price, supplier_id.
        Example JSON:
        {
            "material_code": "M005",
            "material_name": "New Fabric",
            "material_type": "fabric",
            "material_buy_price": 120.0,
            "supplier_id": 1
        }
        """
        try:
            data = request.jsonrequest
            
            if 'material_buy_price' in data and data['material_buy_price'] < 100.0:
                return {'error': 'Material Buy Price cannot be less than 100.', 'status_code' : 400,}

            # Basic validation for required fields
            required_fields = ['material_code', 'material_name', 'material_type', 'material_buy_price', 'supplier_id']
            if not all(field in data for field in required_fields):
                return {'error': 'Missing required fields. Please provide: %s' % ', '.join(required_fields), 'status_code' : 400,}
            
            # Additional validation for material_type
            allowed_types = ['fabric', 'jeans', 'cotton']
            if data.get('material_type').lower() not in allowed_types:
                return {'error': 'Invalid material_type. Allowed types are: fabric, jeans, cotton.', 'status_code' : 400,}
            
            material = request.env['material.material'].sudo().create(data)
            return {
                'id': material.id,
                'message': 'Material created successfully!',
                'status_code' : 201,
            }
        except Exception as e:
            error_message = str(e)
            status_code = 500
            if 'cannot be less than 100' in error_message:
                status_code = 400
            elif 'unique(material_code)' in error_message:
                status_code = 409 # Conflict
            
            return {
                'error': error_message,
                'status_code' : status_code,
            }
        

    @http.route('/api/materials/<int:material_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        """
        API endpoint to update an existing material.
        Example JSON:
        {
            "material_name": "Updated Fabric",
            "material_buy_price": 150.0
        }
        """
        try:
            material = request.env['material.material'].sudo().browse(material_id)
            if not material.exists():
                return {
                        'error': "Material not found",
                        'status_code' : 404,
                    }
            
            data = request.jsonrequest
            if 'material_buy_price' in data and data['material_buy_price'] < 100.0:
                return {'error': 'Material Buy Price cannot be less than 100.', 'status_code' : 400,}

            # Validate material_type if provided
            if 'material_type' in data:
                allowed_types = ['fabric', 'jeans', 'cotton']
                if data.get('material_type').lower() not in allowed_types:
                    return {
                        'error': "Invalid material_type. Allowed types are: fabric, jeans, cotton.",
                        'status_code' : 400,
                    }
            
            material.sudo().write(data)
            return {
                'id': material.id,
                'message': 'Material updated successfully!',
                'status_code' : 200,
            }
        except Exception as e:
            error_message = str(e)
            status_code = 500
            if 'cannot be less than 100' in error_message:
                status_code = 400
            
            return {
                'error': error_message,
                'status_code' : status_code,
            }


    @http.route('/api/materials/<int:material_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id, **kw):
        """
        API endpoint to delete a material.
        """
        try:
            material = request.env['material.material'].sudo().browse(material_id)
            if not material.exists():
                return Response(
                    json.dumps({'error': 'Material not found.'}),
                    headers={'Content-Type': 'application/json'},
                    status=404
                )
            material.sudo().unlink()

            return Response(
                json.dumps({'message': 'Material deleted successfully!'}),
                headers={'Content-Type': 'application/json'},
                status=200
            )
        except Exception as e:
            return Response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=500
            )
# -*- coding: utf-8 -*-
# from odoo import http
import json
from odoo import http, _, exceptions
from odoo.http import content_disposition, request, Response
from odoo.addons.web.controllers.main import Home
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.http import Controller, dispatch_rpc, route
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError
from odoo.tools import config
from odoo.tools.safe_eval import safe_eval

class MaterialApi(http.Controller):
    def _auth(self, authorization):
        if not 'Bearer' in authorization:
            return False
        token = authorization.replace('Bearer ', '')
        if request.env['res.users.apikeys']._check_credentials(scope='rpc', key=token):
            return True
        return False
    
    def eval_request_params(self, kwargs):
        for k, v in kwargs.items():
            try:
                kwargs[k] = safe_eval(v)
            except Exception:
                continue

    @route('/get-material', type='http', auth='public', save_session=False, csrf=False, cors="*", methods=['GET'])
    def search_read(self, **kw):
        self.eval_request_params(kw)
        auth = self._auth(request.httprequest.headers.get('Authorization'))
        if not auth:
            Response.status = '401'
            json_data = json.dumps(
                {'message': f'''Invalid bearer token!'''})
            return Response(json_data, content_type='application/json')
        try:
            materials = request.env['material.material'].sudo().search_read(**kw)
            print(f'''\033[96m{materials}\033[0m''')
            json_data = json.dumps(
                {'results': materials}
            )
            return Response(json_data, content_type='application/json')
        except Exception as e:
            Response.status = '403'
            json_data = json.dumps(
                {'message': str(e)})
            return Response(json_data, content_type='application/json')

    @route('/post-material', type='json', auth='public', save_session=False, csrf=False, cors="*", methods=['POST'])
    def create(self, **kw):
        auth = self._auth(request.httprequest.headers.get('Authorization'))
        if not auth:
            Response.status = '401'
            return {'message': 'Invalid bearer token!'}
        data_material = kw.get('data')
        try:
            with request.env.cr.savepoint():
                results = []
                params = ['name', 'code', 'type', 'buy_price', 'supplier']
                for index, data in enumerate(data_material):
                    # CHECK ALL KEY PARAM
                    for param in params:
                        if param not in data:
                            Response.status = '406'
                            return {'message': f'''Object key [{param}] must be in params index {index}'''}
                    supplier = request.env['res.partner'].sudo().search([('name', '=', data['supplier'])])
                    if not supplier:
                        Response.status = '406'
                        return {'message': f'''Supplier {data['supplier']} not found'''}
                    vals = {
                        'material_code': data['code'],
                        'material_name': data['name'],
                        'material_type': data['type'],
                        'material_buy_price': data['buy_price'],
                        'suplier_partner_id': supplier.id
                    }
                    data_material = request.env['material.material'].sudo().create(vals)
                    results.append([{'material_id': data_material.id, 'nama':data_material.material_name}])
                Response.status = '201'
                return {'data': results, 'message': 'Successfully Created'}
        except Exception as e:
            request.env.cr.rollback()
            Response.status = '403'
            return {'message': str(e)}

    @route('/delete-material', type='http', auth='public', save_session=False, csrf=False, cors="*", methods=['DELETE'])
    def unlink(self, **kw):
        self.eval_request_params(kw)
        auth = self._auth(request.httprequest.headers.get('Authorization'))
        result = []
        if not auth:
            Response.status = '401'
            json_data = json.dumps(
                {'message': f'''Invalid bearer token!'''})
            return Response(json_data, content_type='application/json')
        try:
            materials = request.env['material.material'].sudo().search(kw.get('domain'))
            for material in materials:
                result.append([{'material_id': material.id}])
                material.unlink()
            json_data = json.dumps(
                {'results': result, 'message': 'Successfully Deleted'}
            )
            return Response(json_data, content_type='application/json')
        except Exception as e:
            Response.status = '403'
            json_data = json.dumps(
                {'message': str(e)})
            return Response(json_data, content_type='application/json')
    
    @route('/update-material', type='json', auth='public', save_session=False, csrf=False, cors="*", methods=['PUT'])
    def write(self, **kw):
        auth = self._auth(request.httprequest.headers.get('Authorization'))
        if not auth:
            Response.status = '401'
            return {'message': 'Invalid bearer token!'}
        data_material = kw.get('data')
        try:
            with request.env.cr.savepoint():
                results = []
                params = ['name', 'code', 'type', 'buy_price', 'supplier']
                for index, data in enumerate(data_material):
                # CHECK ALL KEY PARAM
                    for param in params:
                        if param not in data:
                            Response.status = '406'
                            return {'message': f'''Object key [{param}] must be in params index {index}'''}
                    materials = request.env['material.material'].sudo().search([('id', 'in', [x for x in kw.get('ids')])])
                    if not materials:
                        Response.status = '406'
                        return {'message': f'''Material with ids {[x for x in kw.get('ids')]} not found'''}
                    for idx, material in enumerate(materials):
                        datas = kw.get('data')
                        print(f'''\033[96m{material}\033[0m''')

                        supplier = request.env['res.partner'].sudo().search([('name', '=', datas[idx]['supplier'])])
                        if not supplier:
                            Response.status = '406'
                            return {'message': f'''Supplier {datas[idx]['supplier']} not found'''}
                        results.append([{'material_id':material.id}])
                        material.write({
                            'material_code': datas[idx]['code'],
                            'material_name': datas[idx]['name'],
                            'material_type': datas[idx]['type'],
                            'material_buy_price': datas[idx]['buy_price'],
                            'suplier_partner_id': supplier.id
                        })
                Response.status = '201'
                return {'data': results, 'message': 'Successfully Updated'}
        except Exception as e:
            request.env.cr.rollback()
            Response.status = '403'
            return {'message': str(e)}




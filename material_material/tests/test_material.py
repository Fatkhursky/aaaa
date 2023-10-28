from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase
from odoo.tests import tagged, Form

# @tagged('post_install', '-at_install')
class TestMaterial(TransactionCase):
    @classmethod
    def setUpClass(cls):
        print(f'''\033[96m{'ALLOO'}\033[0m''')
        super().setUpClass()
        cls.material_model = cls.env["material.material"]
        cls.supplier_id = cls.env.ref("res.partner")
        # Create material
        cls.add_material = cls._create_material(cls)
        

    def _create_material(self):
        print(f'''\033[96m{'TESSS'}\033[0m''')
        material = self.material_model.create(
            {
                "material_code": "DDP002",
                "material_name": "Celana Emba",
                "material_type": "jeans",
                "material_buy_price": 99,
                "suplier_partner_id": self.supplier_id.id,
            }
        )
        return material

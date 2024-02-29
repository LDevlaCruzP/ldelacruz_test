# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    responsible_id = fields.Many2one('res.users', 'Responsable', tracking=True)

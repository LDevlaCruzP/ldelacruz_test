# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError

class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'
    
    responsible_id = fields.Many2one('res.users', 'Responsable', default=lambda self: self.env.user, required=True)
    
    def _prepare_default_reversal(self, move):
        # override
        values = super(AccountMoveReversal, self)._prepare_create_values(move)
        values.update({ 'responsible_id': self.responsible_id.id })
        return values
# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_open_wizard(self):
        return {
            'name': _('Enviar email a socio'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'wizard.send.topartner',
            'target': 'new',
        }
        
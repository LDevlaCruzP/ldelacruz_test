# -*- coding: utf-8 -*-
from odoo import models, fields, api, Command
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_due_ids = fields.Many2many('account.move', string='Facturas vencidas', compute='_compute_invoice_due_ids')
    invoice_due_count = fields.Integer('Facturas vencidas (cantidad)', compute='_compute_qty_invoices_due')
    
    @api.depends('name')
    def _compute_invoice_due_ids(self):
        self.invoice_due_ids = False
        if not self.ids:
            return
        query = """--sql
            SELECT
                am.partner_id,
                array_agg(am.id) AS invoice_due_ids
            FROM account_move am
            WHERE
                am.state = 'posted'
                AND am.move_type = 'out_invoice'
                AND am.company_id = %s
                AND am.invoice_date_due < %s
            GROUP BY am.partner_id
        """
        params = (self.env.company.id, fields.Date.today())
        self._cr.execute(query, params)
        results = self._cr.dictfetchall()
        for partner in self.filtered('name'):
            # if partner.name:
            partner_results = []
            if results:
                partner_results = list(filter(lambda x: x['partner_id'] == partner.id and x['invoice_due_ids'], results))
            if partner_results:
                partner.invoice_due_ids = [Command.set([inv_id for inv_id in partner_results[0]['invoice_due_ids'] ])]

    @api.depends('invoice_due_ids')
    def _compute_qty_invoices_due(self):
        for rec in self:
            rec.invoice_due_count = len(rec.invoice_due_ids)

    def action_view_partner_invoices_due(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action['domain'] = [
            ('move_type', '=', 'out_invoice'),
            ('id', 'in', self.invoice_due_ids.ids)
        ]
        action['name'] = 'Facturas vencidas'
        action['display_name'] = 'Facturas vencidas'
        action['context'] = {'default_move_type': 'out_invoice', 'move_type': 'out_invoice', 'journal_type': 'sale'}
        return action


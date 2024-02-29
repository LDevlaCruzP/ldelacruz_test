# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class WizardSendTopartner(models.TransientModel):
    _name = 'wizard.send.topartner'
    _description = 'Wizard - send to partner'

    note = fields.Text('Nota ')

    picking_id = fields.Many2one('stock.picking', 'Picking', default=lambda self: self.env.context.get('active_id'), readonly=True)

    file_attachment_ids = fields.Many2many('ir.attachment', string='Carga archivos')

    @api.onchange('picking_id')
    def _onchange_picking_id(self):
        if self.picking_id:
            products_and_unit = ''.join([f"- {line.product_id.display_name} {line.quantity} unidades\n" for line in self.picking_id.move_ids_without_package])
            note = f"""Productos de la transferencia {self.picking_id.name}\n{products_and_unit}"""
            self.note = note

    def action_send(self):
        picking_id = self.picking_id
        partner_id = picking_id.partner_id
        if not partner_id:
            raise UserError(f'📦 El picking {self.picking_id.name} no tiene un socio asignado')
        # if not partner_id.email or not partner_id.email_formatted:
        #     raise UserError(f'El socio {picking_id.partner_id.name} no tiene un correo asignado')
        if not self.env.user.email or not self.env.user.email_formatted:
            raise UserError(f'👨🏻‍🦱 El usuario {self.env.user.name} no tiene un correo asignado')
        error_msg = ""
        try:
            template = self.env.ref('ldelacruz_test_technical.mail_template_products_in_picking').sudo()
            # if not template.mail_server_id:
            #     raise UserError(f'No se tiene un servidor de correo saliente asignado')
            context = {'note_picking': self.note}
            email_values = {
                'email_cc': False,
                'auto_delete': False,
                'message_type': 'user_notification',
                'recipient_ids': [],
                'partner_ids': [],
                'scheduled_date': False,
                'attachment_ids': self.file_attachment_ids.ids,
            }
            template.with_context(**context).send_mail(self.picking_id.id, force_send=True, raise_exception=True, email_values=email_values)
        except Exception as e:
            error_msg = f"{e.args[0]}\n❌ Ha ocurrido un error al enviar el correo, verifique si tiene configurado su servidor de correo saliente"
            raise ValidationError(error_msg)

        # if not error_msg:
        notification_msg = f'✅ Se ha enviado el correo al socio {self.picking_id.partner_id.name}'
        notification_type = 'success'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': notification_type,
                'message': notification_msg,
                'sticky': True,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

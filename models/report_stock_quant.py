# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


class NewReportStockQuant(models.Model):
    _name = 'new.report.stock.quant'
    _description = 'Saldos stock fisico disponible por cada almacen'
    _auto = False
    
    warehouse_id = fields.Many2one('stock.warehouse', 'Almacen')
    # <field name="warehouse_id"/>
    location_id = fields.Many2one('stock.location', 'Ubicaciones')
    product_id = fields.Many2one('product.product', 'Producto')
    category_id = fields.Many2one('product.category', 'Categoria del producto')
    uom_id = fields.Many2one('uom.uom', string='Unidad de Medida')
    stock_quantity_availability = fields.Float('Stock Fisico disponible')
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""--sql
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER () AS id,
                    loc.warehouse_id as warehouse_id,
                    sq.location_id as location_id,
                    sq.product_id as product_id,
                    pt.categ_id as category_id,
                    pt.uom_id as uom_id,
                    SUM(sq.quantity) as stock_quantity_availability
                FROM stock_quant sq
                JOIN stock_location loc ON sq.location_id = loc.id
                JOIN product_template pt ON sq.product_id = pt.id
                JOIN product_category categ ON categ.id = pt.categ_id
                WHERE
                    sq.company_id = %s
                    AND loc.warehouse_id IS NOT NULL
                    AND pt.uom_id IS NOT NULL
                GROUP BY
                    loc.warehouse_id, sq.location_id, sq.product_id, pt.categ_id, pt.uom_id
            )""" % (self._table, self.env.company.id)
        )


""" queda responder la pregunta 2 """
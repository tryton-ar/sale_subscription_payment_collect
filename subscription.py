# This file is part sale_subscription_payment_collect module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, If, Bool


class Subscription(metaclass=PoolMeta):
    __name__ = 'sale.subscription'

    paymode = fields.Many2One('payment.paymode', 'Paymode',
        domain=[
            ('party', '=', If(Bool(Eval('invoice_party',)),
                    Eval('invoice_party'), Eval('party'))),
            ],
        states={
            'readonly': Eval('state') != 'draft',
            })

    @fields.depends('party', 'invoice_party', 'paymode')
    def on_change_party(self):
        super(Subscription, self).on_change_party()

        if not self.invoice_party:
            self.paymode = None
        if self.party:
            if not self.invoice_party:
                if self.party.customer_paymode:
                    self.paymode = self.party.customer_paymode

    @fields.depends('party', 'invoice_party', 'paymode')
    def on_change_invoice_party(self):
        super(Subscription, self).on_change_invoice_party()

        self.paymode = None
        if self.invoice_party:
            if self.invoice_party.customer_paymode:
                self.paymode = self.invoice_party.customer_paymode
        elif self.party:
            if self.party.customer_paymode:
                self.paymode = self.party.customer_paymode

    def _get_invoice(self):
        Configuration = Pool().get('sale.configuration')
        invoice = super()._get_invoice()
        config = Configuration(1)
        if invoice:
            invoice.paymode = self.paymode
            if self.paymode and config.invoice_description:
                invoice.comment = config.invoice_description
                if self.paymode.bank_account:
                    debit = self.paymode.bank_account.rec_name
                    invoice.comment += ' %s' % '{:*>23}'.format(debit[-4:])
                elif self.paymode.credit_number:
                    debit = self.paymode.credit_number
                    invoice.comment += ' %s' % '{:*>16}'.format(debit[-4:])

        return invoice

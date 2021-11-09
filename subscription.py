# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['Subscription']


class Subscription(metaclass=PoolMeta):
    __name__ = 'sale.subscription'
    paymode = fields.Many2One('payment.paymode', 'Paymode',
        domain=[('party', '=', Eval('party', -1))], depends=['party'])

    def __get_paymode(self):
        '''
        Return paymode.
        '''
        if self.party:
            if self.party.customer_paymode:
                self.paymode = self.party.customer_paymode

    @fields.depends('party', 'paymode')
    def on_change_party(self):
        super().on_change_party()
        self.paymode = None
        self.__get_paymode()

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

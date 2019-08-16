# This file is part sale_subscription_payment_collect module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import subscription


def register():
    Pool.register(
        configuration.Configuration,
        configuration.ConfigurationPaymentCollect,
        subscription.Subscription,
        module='sale_subscription_payment_collect', type_='model')

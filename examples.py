"""
## Note: Firstly you should install the library, what else program can't find 'nowpayments' module.

## Clone repository and move to python/site-packages directory.

## In mac: 
- cd /Library/Frameworks/Python.framework/versions/3.x/lib/python3.x/site-packages
- mv /Users/mert/Desktop/nowpayments .
"""

from nowpayments import (
      currency,
      exchanges,
      Plugins,
      Payments,
      NowPaymentsAPI,
      GetPaymentContext
)
from nowpayments.dataclasses import IPNCompatibleResponse

from logging import Logger, WARN

API_KEY: str = "x-api-key"

plugins = Plugins(API_KEY)

class _TempInterface(IPNCompatibleResponse):
        npc: NowPaymentsAPI
        payment: Payments

def main():
    logger = Logger(__name__)
    ipn = plugins.create_payment(
        client_id=123456789,
        amount=34.5,
        price_currency=currency.usd,
        pay_currency=exchanges.eth,
        order_description="Test Payment"
    )

    ipn: _TempInterface

    payment_response = ipn.npc.get(payment_id=ipn.id)
 
    payment_context_call = GetPaymentContext(payment_response, ipn.npc.api_key)
    payment_context = payment_context_call.payment()

    ## you can also get data from response `payment_response.json()` returns python-dict.
    message = """%d ödeme kimliğine sahip ödeme oluşturulmuştur.\nÖdeme: %.2f %s\nÖdeme Durumu: %s\nÖdeme Linki: %s""" % (
          ipn.id,
          payment_context.price_amount,
          payment_context.price_currency.upper(),
          payment_context.payment_status,
          ipn.url
    )
    logger.warning(message)
    return ipn

main()

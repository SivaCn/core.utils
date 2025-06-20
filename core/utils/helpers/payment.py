# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import hmac
import hashlib

from typing import Optional, List
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import razorpay
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.constants import (
    const_currency,
)
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


class RazorPay:

    #
    # TODO: read these from .env file
    RAZORPAY_KEY_ID = ""
    RAZORPAY_KEY_SECRET = ""
    RAZORPAY_WEBHOOK_SECRET = ""

    def __init__(self,
                 tenant: str,
                 user_slug: str,
                 cart_slug: str,
                 payment_slug: str):

        self.tenant = tenant
        self.user_slug = str(user_slug)
        self.cart_slug = str(cart_slug)
        self.payment_slug = str(payment_slug)

        self.client = razorpay.Client(
            auth=(self.RAZORPAY_KEY_ID, self.RAZORPAY_KEY_SECRET)
        )

    def normalize_amount(self, amount: float, currency: str) -> int:
        """
        Calculates the correct Razorpay amount based on currency type.

        Note: (As per the razorpay document)

            Payment amount in the smallest currency subunit. For example, if the amount to be charged is ₹299.00,
            then pass 29900 in this field. In the case of three decimal currencies, such as KWD, BHD and OMR,
            to accept a payment of 295.991, pass the value as 295990. And in the case of zero decimal currencies
            such as JPY, to accept a payment of 295, pass the value as 295.

            Watch Out!
                As per payment guidelines, you should pass the last decimal number as 0 for three decimal
                currency payments. For example, if you want to charge a customer 99.991 KD for a transaction,
                you should pass the value for the amount parameter as 99990 and not 99991.

        """
        three_decimal_currencies = ['KWD', 'BHD', 'OMR']
        zero_decimal_currencies = ['JPY']

        if currency in zero_decimal_currencies:
            # No adjustment needed
            return int(amount)

        elif currency in three_decimal_currencies:
            # Multiply by 1000, then floor to nearest 10
            adjusted_amount = int(amount * 1000)
            adjusted_amount = (adjusted_amount // 10) * 10  # Truncate last digit
            return adjusted_amount

        else:
            # Default: Multiply by 100 (standard 2-decimal currencies)
            return int(amount * 100)

    def create_order(self,
                     amount: int,
                     currency: Optional[str] = const_currency.INR[0]) -> dict:

        amount = self.normalize_amount(amount=amount, currency=currency)

        order_data = {
            'amount': amount,
            'currency': currency,
            'receipt': f'',
            'notes': {
                'tenant': self.tenant,
                'user_slug': self.user_slug,
                'cart_slug': self.cart_slug,
                'payment_slug': self.payment_slug,
            }
        }

        order = self.client.order.create(data=order_data)
        '''{'amount': 2103,
            'amount_due': 2103,
            'amount_paid': 0,
            'attempts': 0,
            'created_at': 1750358975,
            'currency': 'INR',
            'entity': 'order',
            'id': 'order_Qj9wYrLhXykD93',
            'notes': {'cart_slug': 'f8bf41d9-96fb-46b2-971a-7042f89d205e',
                      'payment_slug': '14deab4e-b918-447c-ac26-c10ac002bf3c',
                      'tenant': 'yellow',
                      'user_slug': '8262356b-e085-4faa-a073-c09be675d256'},
            'offer_id': None,
            'receipt': None,
            'status': 'created'}
        '''

        return {
            'order_id': order['id'],
            'status': order['status'],
            'notes': order['notes'],
            'receipt': order['receipt'],
            'response_dump': order,
        }


    def verify_signature(self,
                         order_id: str,
                         payment_id: str,
                         signature: str) -> bool:

        # Create expected signature using backend secret key
        expected_signature = hmac.new(
            self.RAZORPAY_WEBHOOK_SECRET.encode('utf-8'),
            msg=f"{order_id}|{payment_id}".encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(expected_signature, signature):
            return True

        return False


#
# Get the Payment Partner Class
PayPartner = {
    'razorpay': RazorPay,
}['razorpay']


"""
## Dataclasses ##
Belongs dataclasses in NowPayments library.

- Invoice Dataclass
- Payment Dataclass
- InvoicePayment Dataclass

Defined dataclasses has same attributes with API response fields.

Example:
response = {price_amount: Any, price_currency: Any, order_id: Any, order_description: Any, ipn_callback_url: Any, success_url: Any, cancel_url: Any
}

invoice = Invoice(**response) # this will return a Invoice object that has all fields

#### Note: Field values has to be same type with attribute types in dataclass interface. ####
"""

from pydantic.dataclasses import dataclass


@dataclass
class Invoice:
  price_amount: float | int
  price_currency: str
  order_id: str
  order_description: str
  ipn_callback_url: str
  success_url: str
  cancel_url: str
  
  @property
  def data(self):
      return dict(self.__dict__)


@dataclass
class Payment:
  iid: int
  pay_currency: str
  order_description: str
  
  @property
  def data(self):
      return dict(self.__dict__)


@dataclass
class InvoicePayment:
    payment_id: int
    payment_status: str
    pay_address: str
    price_amount: float | int
    price_currency: str
    pay_amount: float | int
    amount_received: bool
    pay_currency: str
    order_id: str
    order_description: str
    ipn_callback_url: str
    created_at: str
    updated_at: str
    purchase_id: int
    smart_contract: str 
    network: str
    network_precision: str
    time_limit: int
    burning_percent: float | int
    expiration_estimate_date: str
    is_fixed_rate: str
    is_fee_paid_by_user: str
    valid_until: str
    type: str
    
    @property
    def data(self) -> dict:
        return dict(self.__dict__)
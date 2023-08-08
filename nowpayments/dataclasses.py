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
from typing import Any

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
      for k,v in self.__dict__.copy().items():
         if k.startswith("_"):
            self.__dict__.pop(k)
      for k,v in self.__dict__.copy().items():
         if k.startswith("_"):
            self.__dict__.pop(k)
      return dict(self.__dict__)


@dataclass
class Payment:
  iid: int
  pay_currency: str
  order_description: str
  
  @property
  def data(self):
      for k,v in self.__dict__.copy().items():
         if k.startswith("_"):
            self.__dict__.pop(k)
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
        for k,v in self.__dict__.copy().items():
          if k.startswith("_"):
            self.__dict__.pop(k)
        return dict(self.__dict__)
  

@dataclass
class IPNCompatibleResponse:
    id: int = Any
    npc: Any = Any
    url: str = Any
    invoice: Any = Any
    payment: Any = Any
    qr: str | bytes = Any

    def __init__(self, *args, **kwargs):
       for k,v in kwargs.items():
          setattr(self, k, v)
       condition = all(
        filter(
          lambda x: not x[0].startswith("_"), 
          self.__dict__.items()
        )
        )
       assert (condition), "All fields must be filled."
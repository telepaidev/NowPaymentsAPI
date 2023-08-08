"""
## Introduction ##
Welcome to NowPaymentsAPI Wrapper, lets start to create payments.

### Base Classes & Methods ###
- NowPaymentsAPI(api_key: str)
- InvoiceContext(response: Response, api_key: str)
- PaymentContext(response: Response, api_key: str)
- GetPaymentContext(response: Response, api_key: str)

- Invoices(payment: Payment, api_key: str)
- Payments(payment: Payment, api_key: str)

"""

from requests import get, post, Response
from pydantic import BaseModel
from enum import Enum, auto
from PIL.Image import Image
from qrcode import make
from io import BytesIO
from typing import Literal, Union, Any, List, Dict, NoReturn
from .dataclasses import (
     Invoice,
     Payment,
     InvoicePayment
)

class mimetypes(Enum):
    png: "mimetypes.png" = auto()
    jpg: "mimetypes.jpg" = auto()
    jpeg: "mimetypes.jpeg" = auto()

class types(Enum):
    invoice: "types.invoice" = auto()
    payment: "types.payment" = auto()
    invoice_payment: "types.invoice_payment" = auto()

class databases(Enum):
    users: "databases.users" = auto()
    payment_requests: "databases.payment_requests" = auto()

class payment_requests(Enum):
    add_fund: "payment_requests.add_fund" = auto()

class methods(Enum):
    get: "methods.get" = auto()
    post: "methods.post" = auto()

class Model(BaseModel):
    data: Union[List[Any], Dict[str, Any]]
    __doc__ = "Base class for instances"

class ImageSaved(Image):
    __doc__ = "Class created to saying image saved successfully"


class NowPaymentsAPI:
    base_url = "https://api.nowpayments.io/v1"
    api_key: str
    def __init__(self, api_key: str) -> NoReturn:
        self.api_key = api_key
        assert (api_key), "You have to pass API Key to access NowPayments API Features"
        self.headers = {"x-api-key": self.api_key, 'Content-Type': 'application/json'}
    
    def request(self, method: methods, base_url: str, headers: dict = {}, *args, **kwargs):
        if not headers:
            headers = self.headers
        if   method == methods.get:
            return get(base_url, *args, **kwargs, headers=headers)
        elif method == methods.post:
            return post(base_url, *args, **kwargs, headers=headers)
    
    def create(self, type: types, instance: Model, headers: dict):
        self.headers.update(headers)
        if type is types.invoice:
            return self.request(method=methods.post, base_url=f"{self.base_url}/{type.name}", json=instance.data, headers=headers)
        elif type is types.payment:
            return self.request(method=methods.post, base_url=f"{self.base_url}/{type.name}", json=instance.data, headers=headers)
        elif type is types.invoice_payment:
            name = type.name.replace("_", "-")
            return self.request(method=methods.post, base_url=f"{self.base_url}/{name}", json=instance.data, headers=headers)
    def get(self, payment_id: int, type: types = types.payment):
            base_url = f"{self.base_url}/{type.name}/{payment_id}"
            return self.request(method=methods.get, base_url=base_url, headers=self.headers)


class PaymentContext(NowPaymentsAPI, InvoicePayment):
    def __init__(self, response: Response, api_key: str) -> NoReturn:
            self.response = response
            super().__init__(api_key)

            for k, v in self.data.items():
                setattr(self, k, v)
    @property
    def data(self) -> dict:
        return self.response.json()
    
    def payment(self):
        response = self.get(payment_id=self.data.get("payment_id"))
        return GetPaymentContext(response=response, api_key=self.api_key)
    
    def qr(self, image: str = None, file_extension: mimetypes = mimetypes.png, fstream: bool = False) -> ImageSaved | BytesIO:
        assert bool(isinstance(file_extension, (str, mimetypes))), \
            "File extension must be instance of str or mimetypes enum member."
        assert ("\\" in image), \
            "Image path can not include backslash/pipe character."
       
        if not image:
            image = f"./{self.order_id}.{file_extension if isinstance(file_extension, str) else file_extension.name}"
        qr: Image = make(self.pay_address)
        qr.save(image)

        if fstream:
            io =BytesIO(open(image, "rb"))
            io.name = image.split("/")[-1]
            return io
        return image
    def create_payment_url(self, invoice: "InvoiceContext"):
        return "%s&paymentId=%s" % (
            invoice.invoice_url,
            self.payment_id
        )
            

class InvoiceContext(NowPaymentsAPI, Invoice): 
    id: int
    token_id: int
    order_id: str
    order_description: str
    price_amount: float | int
    price_currency: str
    pay_currency: str
    ipn_callback_url: str
    invoice_url: str
    success_url: str
    cancel_url: str
    partially_paid_url: str
    payout_currency: str
    created_at: str
    updated_at: str
    is_fixed_rate: bool
    is_fee_paid_by_user: bool
    def __init__(self, response: Response, api_key: str) -> NoReturn:
            self.response = response
            super().__init__(api_key)

            for k, v in self.data.items():
                setattr(self, k, v)
        
    @property
    def data(self) -> dict:
            return self.response.json()
        
    def payment(self):
            response = self.get(payment_id=self.data.get("payment_id"))
            return GetPaymentContext(response=response, api_key=self.api_key)

class GetPaymentContext(NowPaymentsAPI):
    payment_id: int 
    invoice_id: int
    payment_status: str | Union[Literal["finished"], Literal["cancelled"]]
    pay_address: str
    payin_extra_id: int
    price_amount: float | int
    price_currency: str
    pay_amount: float | int
    actually_paid: float | int
    pay_currency: str
    order_id: str
    order_description: str
    purchase_id: int
    outcome_amount: float | int
    outcome_currency: str
    payout_hash: str
    payin_hash: str
    created_at: str
    updated_at: str
    burning_percent: float | int
    type: str
    def __init__(self, response: Response, api_key: str) -> NoReturn:
        self.response = response
        super().__init__(api_key)

        for k, v in self.data.items():
            setattr(self, k, v)
    
    @property
    def data(self) -> dict:
        return self.response.json()
    
    def payment(self):
        response = self.get(payment_id=self.data.get("payment_id"))
        return GetPaymentContext(response=response, api_key=self.api_key)



class Invoices(NowPaymentsAPI, Invoice):
    def __init__(self, invoice: Invoice, api_key: str) -> NoReturn:
        super().__init__(api_key)
        self.invoice = invoice

    def create_invoice(self):
        response = self.create(type=types.invoice, instance=self.invoice, headers=self.headers)
        return InvoiceContext(response=response, api_key=self.api_key)
    

class Payments(NowPaymentsAPI):
    def __init__(self, payment: Payment, api_key: str) -> NoReturn:
        super().__init__(api_key)
        self.payment = payment

    def create_payment(self):
        response = self.create(type=types.invoice_payment, instance=self.payment, headers=self.headers)
        return PaymentContext(response=response, api_key=self.api_key)
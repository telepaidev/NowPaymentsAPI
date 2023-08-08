# NowPaymentsAPI

An official API wrapper for NowPayments.

Check this gists for example: [click](https://gist.github.com/fswair/cac346b06a61f93c1d24941bc6b56877)

## Introduction

Welcome to NowPaymentsAPI Wrapper, lets start to create payments.

### Base Classes & Methods

- NowPaymentsAPI(api_key: str)
- InvoiceContext(response: Response, api_key: str)
- PaymentContext(response: Response, api_key: str)
- GetPaymentContext(response: Response, api_key: str)

- Invoices(payment: Payment, api_key: str)
- Payments(payment: Payment, api_key: str)

## Dataclasses

Belongs dataclasses in NowPayments library.

- Invoice Dataclass
- Payment Dataclass
- InvoicePayment Dataclass

Defined dataclasses has same attributes with API response fields.

Example:
response = {price_amount: Any, price_currency: Any, order_id: Any, order_description: Any, ipn_callback_url: Any, success_url: Any, cancel_url: Any
}

invoice = Invoice(\*\*response) # this will return a Invoice object that has all fields

#### Note: Field values has to be same type with attribute types in dataclass interface.

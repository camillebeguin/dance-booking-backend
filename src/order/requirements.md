## Product catalog

- Customers can purchase single credits or credit packages. Credits can be used in any studio.
- Packages have a fixed validity period (10 credits - 3 months, 20 credits - 4 months, 50 credits - 6 months).
- A customer is the equivalent of Students in the Booking bounded context.

## Payment methods

- Customers can add a new payment method.
- Customers can replace their current payment method.
- Customers can deactivate a payment method.
- Customers can list payment methods.

## Orders/payments

- An order can only be initiated if the customer has a registered and non-expired payment method.
- Only card payments are supported.
- Payments are fulfilled thanks to a PSP integration (payment services provider).
- Order fails if the payment fails instantly.
- Order fails if the payment fails after being attempted.
- Order is completed if the payment succeeds.
- Once an order is completed, the customer must receive a confirmation email.
- Once an order is completed, the Student must be credited accordingly in the Booking context.

## Discounts

- Students can apply for discounts ("university" students, job seeker, "intermittent du spectacle") and use those discounts when purchasing credits.
- Students can submit proof documents when applying for a discount.
- Discounts are in pending state, and can be either approved or rejected.
- Only approved discounts can be used when purchasing credits.
- Discounts can be approved for a fixed period and can no longer be used once they expire.

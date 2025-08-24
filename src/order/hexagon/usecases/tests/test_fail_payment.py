import pytest
from order.adapters.gateways.repositories.mock_order_repository import (
    MockOrderRepository,
)
from order.adapters.gateways.repositories.mock_payment_repository import (
    MockPaymentRepository,
)
from order.hexagon.models.payment import Payment, PaymentStatus
from order.hexagon.models.order import Order, OrderStatus, OrderItem
from shared_kernel.utils import euuid
from order.hexagon.usecases.fail_payment import FailPaymentUseCase
from order.hexagon.models.money import Money, SupportedCurrency


@pytest.fixture
def context():
    return {
        "order_repository": MockOrderRepository(),
        "payment_repository": MockPaymentRepository(),
    }


def test_failed_payment_should_fail_order(context):
    context["order_repository"].feed_with(
        [
            Order(
                id=euuid("order"),
                account_id=euuid("account"),
                status=OrderStatus.confirmed,
                items=[
                    OrderItem(
                        product_id=euuid("single_credit"),
                        price=Money(amount=100, currency=SupportedCurrency.EUR),
                    )
                ],
            ),
        ]
    )

    context["payment_repository"].feed_with(
        [
            Payment(
                id=euuid("order"),
                status=PaymentStatus.pending,
                payment_intent_id="intent",
                amount=Money(amount=100, currency=SupportedCurrency.EUR),
            )
        ]
    )

    FailPaymentUseCase(
        order_repository=context["order_repository"],
        payment_repository=context["payment_repository"],
    ).execute(payment_intent_id="intent")

    assert context["order_repository"].orders == [
        Order(
            id=euuid("order"),
            account_id=euuid("account"),
            status=OrderStatus.failed,
            items=[
                OrderItem(
                    product_id=euuid("single_credit"),
                    price=Money(amount=100, currency=SupportedCurrency.EUR),
                )
            ],
        )
    ]

    assert context["payment_repository"].payments == [
        Payment(
            id=euuid("order"),
            status=PaymentStatus.failed,
            payment_intent_id="intent",
            amount=Money(amount=100, currency=SupportedCurrency.EUR),
        )
    ]

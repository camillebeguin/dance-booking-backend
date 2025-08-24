import pytest
from unittest.mock import ANY
from order.adapters.gateways.repositories.mock_order_repository import (
    MockOrderRepository,
)
from order.adapters.gateways.repositories.mock_payment_repository import (
    MockPaymentRepository,
)
from order.hexagon.models.payment import Payment, PaymentStatus
from order.hexagon.models.order import Order, OrderStatus, OrderItem, OrderEventType
from shared_kernel.utils import euuid
from order.hexagon.usecases.succeed_payment import (
    SucceedPaymentUseCase,
)
from order.hexagon.models.money import Money, SupportedCurrency
from order.adapters.gateways.repositories.mock_event_repository import (
    MockEventRepository,
)
from order.hexagon.models.event import DomainEvent


@pytest.fixture
def context():
    return {
        "order_repository": MockOrderRepository(),
        "payment_repository": MockPaymentRepository(),
        "event_repository": MockEventRepository(),
    }


def test_succeeded_payment_should_complete_order(context):
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

    SucceedPaymentUseCase(
        order_repository=context["order_repository"],
        payment_repository=context["payment_repository"],
        event_repository=context["event_repository"],
    ).execute(payment_intent_id="intent")

    assert context["order_repository"].orders == [
        Order(
            id=euuid("order"),
            account_id=euuid("account"),
            status=OrderStatus.completed,
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
            status=PaymentStatus.succeeded,
            payment_intent_id="intent",
            amount=Money(amount=100, currency=SupportedCurrency.EUR),
        )
    ]

    assert context["event_repository"].events == [
        DomainEvent(
            id=ANY,
            type=OrderEventType.order_completed,
            data={"order_id": euuid("order")},
        )
    ]

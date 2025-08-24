import pytest
from order.adapters.gateways.repositories.mock_order_repository import (
    MockOrderRepository,
)
from order.hexagon.models.order import Order, OrderStatus, OrderItem
from shared_kernel.utils import euuid
from order.hexagon.usecases.confirm_order import ConfirmOrderUseCase
from order.adapters.gateways.providers.mock_payment_provider import (
    MockPaymentProvider,
)
from order.adapters.gateways.repositories.mock_payment_repository import (
    MockPaymentRepository,
)
from order.hexagon.models.exceptions import OrderAlreadyConfirmedException
from order.hexagon.models.payment import Payment, PaymentStatus
from order.hexagon.models.money import Money, SupportedCurrency


@pytest.fixture
def context():
    return {
        "order_repository": MockOrderRepository(),
        "payment_provider": MockPaymentProvider(
            keys_to_payment_intents={
                euuid("order"): "intent",
            }
        ),
        "payment_repository": MockPaymentRepository(),
    }


def test_can_confirm_order(context):
    context["order_repository"].feed_with(
        [
            Order(
                id=euuid("order"),
                account_id=euuid("account"),
                status=OrderStatus.started,
                items=[
                    OrderItem(
                        product_id=euuid("single_credit"),
                        price=Money(amount=100, currency=SupportedCurrency.EUR),
                    )
                ],
            ),
        ]
    )

    ConfirmOrderUseCase(
        order_repository=context["order_repository"],
        payment_provider=context["payment_provider"],
        payment_repository=context["payment_repository"],
    ).execute(order_id=euuid("order"))

    assert context["order_repository"].orders == [
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
        )
    ]

    assert context["payment_repository"].payments == [
        Payment(
            id=euuid("order"),
            status=PaymentStatus.pending,
            payment_intent_id="intent",
            amount=Money(amount=100, currency=SupportedCurrency.EUR),
        )
    ]


def test_can_confirm_order_only_once(context):
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

    with pytest.raises(OrderAlreadyConfirmedException):
        ConfirmOrderUseCase(
            order_repository=context["order_repository"],
            payment_provider=context["payment_provider"],
            payment_repository=context["payment_repository"],
        ).execute(order_id=euuid("order"))


def test_can_confirm_order_with_multiple_items(context):
    context["order_repository"].feed_with(
        [
            Order(
                id=euuid("order"),
                account_id=euuid("account"),
                status=OrderStatus.started,
                items=[
                    OrderItem(
                        product_id=euuid("single_credit"),
                        price=Money(amount=100, currency=SupportedCurrency.EUR),
                    ),
                    OrderItem(
                        product_id=euuid("single_credit"),
                        price=Money(amount=300, currency=SupportedCurrency.EUR),
                    ),
                ],
            ),
        ]
    )

    ConfirmOrderUseCase(
        order_repository=context["order_repository"],
        payment_provider=context["payment_provider"],
        payment_repository=context["payment_repository"],
    ).execute(order_id=euuid("order"))

    assert context["order_repository"].orders == [
        Order(
            id=euuid("order"),
            account_id=euuid("account"),
            status=OrderStatus.confirmed,
            items=[
                OrderItem(
                    product_id=euuid("single_credit"),
                    price=Money(amount=100, currency=SupportedCurrency.EUR),
                ),
                OrderItem(
                    product_id=euuid("single_credit"),
                    price=Money(amount=300, currency=SupportedCurrency.EUR),
                ),
            ],
        )
    ]

    assert context["payment_repository"].payments == [
        Payment(
            id=euuid("order"),
            status=PaymentStatus.pending,
            payment_intent_id="intent",
            amount=Money(amount=400, currency=SupportedCurrency.EUR),
        )
    ]

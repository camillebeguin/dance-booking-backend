from order.hexagon.usecases.create_order import CreateOrderUseCase
import pytest
from shared_kernel.utils import euuid
from order.hexagon.models.order import Order, OrderStatus, OrderItem
from order.adapters.gateways.repositories.mock_order_repository import (
    MockOrderRepository,
)
from order.adapters.gateways.repositories.mock_product_repository import (
    MockProductRepository,
)
from order.hexagon.models.product import Product
from order.hexagon.models.money import Money
from order.hexagon.models.money import SupportedCurrency


@pytest.fixture
def context():
    return {
        "order_repository": MockOrderRepository(),
        "product_repository": MockProductRepository(),
    }


def test_can_create_order(context):
    context["order_repository"].feed_with([])
    context["product_repository"].feed_with(
        [
            Product(
                id=euuid("single_credit"),
                current_price=Money(amount=100, currency=SupportedCurrency.EUR),
            )
        ]
    )

    CreateOrderUseCase(
        order_repository=context["order_repository"],
        product_repository=context["product_repository"],
    ).execute(
        order_id=euuid("order"),
        account_id=euuid("account"),
        product_ids=[euuid("single_credit")],
    )

    assert context["order_repository"].orders == [
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
        )
    ]

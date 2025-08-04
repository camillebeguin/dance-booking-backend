from payment.hexagon.usecases.order_credit import OrderCreditUseCase
import pytest
from shared_kernel.utils import euuid
from payment.hexagon.models.order import Order, OrderStatus
from payment.adapters.gateways.repositories.mock_order_repository import (
    MockOrderRepository,
)


@pytest.fixture
def context():
    return {
        "order_repository": MockOrderRepository(),
    }


def test_can_order_single_credit(context):
    context["order_repository"].feed_with([])

    OrderCreditUseCase(
        order_repository=context["order_repository"],
    ).execute(
        order_id=euuid("order"),
        account_id=euuid("account"),
    )

    assert context["order_repository"].orders == [
        Order(
            id=euuid("order"),
            account_id=euuid("account"),
            status=OrderStatus.started,
        )
    ]

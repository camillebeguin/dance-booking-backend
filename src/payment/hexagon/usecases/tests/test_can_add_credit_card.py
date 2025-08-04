import pytest
from hexagon.models.account import Account
from shared_kernel. import euuid


@pytest.fixture
def context():
    return {}


def test_can_add_credit_card(context):
    context["account_repository"].feed_with(
        [
            Account(
                id=euuid("account"),
                student_id=euuid("student"),
            ),
        ]
    )

import pytest
from booking.hexagon.models.studio import Studio, StudioAddress
from booking.hexagon.usecases.create_studio import (
    CreateStudioUseCase,
    CreateStudioInput,
    CreateStudioAddressInput,
)
from booking.adapters.gateways.repositories.mock_studio_repository import (
    MockStudioRepository,
)
from shared_kernel.utils import euuid


@pytest.fixture
def context():
    return {
        "studio_repository": MockStudioRepository(),
    }


def test_can_create_studio(context):
    context["studio_repository"].feed_with([])

    CreateStudioUseCase(
        studio_repository=context["studio_repository"],
    ).execute(
        input=CreateStudioInput(
            id=euuid("studio"),
            name="Studio 1",
            address=CreateStudioAddressInput(
                street="123 Main St",
                city="Anytown",
                state="CA",
                zip_code="12345",
                country="USA",
            ),
        ),
    )

    assert context["studio_repository"].studios == [
        Studio(
            id=euuid("studio"),
            name="Studio 1",
            address=StudioAddress(
                street="123 Main St",
                city="Anytown",
                state="CA",
                zip_code="12345",
                country="USA",
            ),
            rooms=[],
        ),
    ]

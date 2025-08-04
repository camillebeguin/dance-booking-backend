from booking.hexagon.models.studio import Studio, StudioAddress
from uuid import UUID
from booking.hexagon.gateways.repositories.studio_repository import StudioRepository
from pydantic import BaseModel


class CreateStudioAddressInput(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str


class CreateStudioInput(BaseModel):
    id: UUID
    name: str
    address: CreateStudioAddressInput


class CreateStudioUseCase:
    def __init__(self, studio_repository: StudioRepository):
        self.studio_repository = studio_repository

    def execute(self, input: CreateStudioInput):
        studio = Studio.create(
            id=input.id,
            name=input.name,
            address=StudioAddress(
                street=input.address.street,
                city=input.address.city,
                state=input.address.state,
                zip_code=input.address.zip_code,
                country=input.address.country,
            ),
        )

        self.studio_repository.save(studio)

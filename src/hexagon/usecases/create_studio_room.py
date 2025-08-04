from hexagon.gateways.repositories.studio_repository import StudioRepository
from uuid import UUID
from pydantic import BaseModel


class CreateStudioRoomInput(BaseModel):
    id: UUID
    studio_id: UUID
    name: str
    capacity: int


class CreateStudioRoomUseCase:
    def __init__(self, studio_repository: StudioRepository):
        self.studio_repository = studio_repository

    def execute(self, input: CreateStudioRoomInput):
        studio = self.studio_repository.get_by_id(input.studio_id)
        studio.create_room(input.id, input.name, input.capacity)
        self.studio_repository.save(studio)

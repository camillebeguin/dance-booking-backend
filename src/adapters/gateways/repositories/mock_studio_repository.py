from hexagon.gateways.repositories.studio_repository import StudioRepository
from hexagon.models.studio import Studio
from uuid import UUID


class MockStudioRepository(StudioRepository):
    def __init__(self):
        self.studios: list[Studio] = []

    def feed_with(self, studios: list[Studio]):
        self.studios = studios

    def get_by_id(self, id: UUID) -> Studio:
        return next((studio for studio in self.studios if studio.id == id), None)

    def save(self, studio: Studio):
        if studio.id in [s.id for s in self.studios]:
            self.studios[self.studios.index(studio)] = studio
        else:
            self.studios.append(studio)

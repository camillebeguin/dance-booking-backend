from dataclasses import dataclass
from uuid import UUID

from booking.hexagon.models.exceptions import StudioRoomAlreadyExists


@dataclass
class StudioAddress:
    street: str
    city: str
    state: str
    zip_code: str
    country: str


@dataclass
class StudioRoom:
    id: UUID
    name: str
    capacity: int


@dataclass
class Studio:
    id: UUID
    name: str
    address: StudioAddress
    rooms: list[StudioRoom]

    @staticmethod
    def create(id: UUID, name: str, address: StudioAddress):
        return Studio(id=id, name=name, address=address, rooms=[])

    def create_room(self, id: UUID, name: str, capacity: int):
        if any(room.name == name for room in self.rooms):
            raise StudioRoomAlreadyExists

        self.rooms.append(StudioRoom(id=id, name=name, capacity=capacity))

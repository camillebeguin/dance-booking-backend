from sqlalchemy import Column, ForeignKey, String, Integer, UUID
from uuid import uuid4
from booking.adapters.gateways.repositories.sql_entities.sql_base import BaseModel
from sqlalchemy.orm import relationship
from booking.hexagon.models.studio import Studio, StudioAddress, StudioRoom


class SqlStudio(BaseModel):
    __tablename__ = "studios"

    address_id = Column(ForeignKey("studio_addresses.id"), nullable=False)
    name = Column(String, nullable=False)

    address = relationship("SqlAddress", uselist=False)
    studio_rooms = relationship("SqlStudioRoom")

    def to_domain_model(self) -> Studio:
        return Studio(
            id=self.id,
            name=self.name,
            address=self.address.to_domain_model(),
            rooms=[room.to_domain_model() for room in self.studio_rooms],
        )

    @classmethod
    def from_domain_model(cls, studio: Studio) -> "SqlStudio":
        return cls(
            id=studio.id,
            name=studio.name,
            address=SqlAddress.from_domain_model(studio.address),
            studio_rooms=[
                SqlStudioRoom.from_domain_model(room) for room in studio.rooms
            ],
        )


class SqlStudioRoom(BaseModel):
    __tablename__ = "studio_rooms"

    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    studio_id = Column(ForeignKey("studios.id"), nullable=False)
    studio = relationship("SqlStudio", back_populates="studio_rooms")

    def to_domain_model(self) -> StudioRoom:
        return StudioRoom(
            id=self.id,
            name=self.name,
            capacity=self.capacity,
        )

    @classmethod
    def from_domain_model(cls, room: StudioRoom) -> "SqlStudioRoom":
        return cls(
            id=room.id,
            name=room.name,
            capacity=room.capacity,
        )


class SqlAddress(BaseModel):
    __tablename__ = "studio_addresses"
    id = Column(UUID, primary_key=True, default=uuid4)

    street = Column(String, nullable=False)

    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)

    def to_domain_model(self) -> StudioAddress:
        return StudioAddress(
            street=self.street,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            country=self.country,
        )

    @classmethod
    def from_domain_model(cls, address: StudioAddress) -> "SqlAddress":
        return cls(
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            country=address.country,
        )

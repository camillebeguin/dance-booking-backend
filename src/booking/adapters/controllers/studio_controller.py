from fastapi import APIRouter, Depends
from src.booking.adapters.dependencies.get_session import get_db_session
from src.booking.adapters.gateways.repositories.sql_studio_repository import (
    SqlStudioRepository,
)
from src.booking.hexagon.usecases.create_studio import (
    CreateStudioUseCase,
    CreateStudioInput,
)
from sqlalchemy.orm import Session

studio_router = APIRouter(prefix="/studio")


def get_create_studio_use_case(session: Session = Depends(get_db_session)):
    return CreateStudioUseCase(
        studio_repository=SqlStudioRepository(session=session),
    )


@studio_router.post("")
def create_studio(
    studio: CreateStudioInput,
    use_case: CreateStudioUseCase = Depends(get_create_studio_use_case),
):
    return use_case.execute(studio)

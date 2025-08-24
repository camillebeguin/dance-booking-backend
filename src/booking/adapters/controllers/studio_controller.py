from fastapi import APIRouter, Depends
from booking.adapters.dependencies.get_session import get_db_session
from booking.adapters.gateways.repositories.sql_studio_repository import (
    SqlStudioRepository,
)
from booking.hexagon.usecases.create_studio import (
    CreateStudioUseCase,
    CreateStudioInput,
)
from sqlalchemy.orm import Session

studio_router = APIRouter(prefix="/studio")


def get_create_studio_use_case(session: Session = Depends(get_db_session)):
    return CreateStudioUseCase(
        studio_repository=SqlStudioRepository(session=session),
    )


@studio_router.post("", status_code=201, response_model=None)
def create_studio(
    studio: CreateStudioInput,
    use_case: CreateStudioUseCase = Depends(get_create_studio_use_case),
):
    return use_case.execute(studio)

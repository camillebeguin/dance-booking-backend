from fastapi import FastAPI
from booking.adapters.controllers.studio_controller import studio_router

app = FastAPI()

app.include_router(studio_router)

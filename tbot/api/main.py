from typing import List

from fastapi import FastAPI, status, Response

from tbot import schemas
from tbot.bot import get_bot
from tbot.utils import (list_relevant_users_for_event, list_house, list_event,
                        create_event, update_event, delete_event)
from tbot.listeners import event_handler  # noqa

app = FastAPI()
bot = get_bot()


@app.get("/users/", response_model=List[schemas.User],
         status_code=status.HTTP_200_OK)
def list_users() -> List[schemas.User]:
    return list_relevant_users_for_event()


@app.get("/houses/", response_model=List[schemas.House],
         status_code=status.HTTP_200_OK)
def list_houses() -> List[schemas.House]:
    return list_house()


@app.get("/events/", response_model=List[schemas.Event],
         status_code=status.HTTP_200_OK)
def list_events() -> List[schemas.Event]:
    events = list_event()
    return events


@app.put("/events/", response_model=schemas.Event,
         status_code=status.HTTP_201_CREATED)
def create_events(event: schemas.EventCreate) -> dict:
    return create_event(event)


@app.patch("/events/", response_model=schemas.Event,
           status_code=status.HTTP_200_OK)
def update_events(event: schemas.EventUpdate) -> dict:
    return update_event(event)


@app.delete("/events/", status_code=status.HTTP_204_NO_CONTENT)
def delete_events(id: int) -> None:
    delete_event(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# get all the events
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.schemas.event import EventResponse

from app.core.database import get_db

from app.services.event import EventService

from app.models.event import Event

router = APIRouter()

# get list of events
@router.get("/v1/event/get-all", status_code=status.HTTP_200_OK)
def get_all_events(request: Request, db:Session =Depends(get_db)):
    eventservice = EventService(db=db)

    result = eventservice.get_all_events()
    return result 


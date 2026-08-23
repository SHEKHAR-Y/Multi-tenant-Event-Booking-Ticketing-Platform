from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas.event import EventCreateRequest, EventCreateResponse
from app.core.security import oauth2_scheme
from app.services.event import create_event_service
from app.core.database import get_db

router = APIRouter()

@router.post("/create", response_model=EventCreateResponse, status_code=status.HTTP_201_CREATED)
def create_event(request: Request, event_request: EventCreateRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    # check if the user exist -> ensure token is valid if yess then just fetch user from token and fetch user role -> if role is organizer
    # then allow the user to create the event else raise error of forbidden 

    res =  create_event_service(event_request, token, db)
    return EventCreateResponse(
        organizer_id=res.organizer_id,
        title=res.title,
        description=res.description,
        venue_name=res.venue_name,
        venue_address=res.venue_address,
        start_time=res.start_time,
        end_time=res.end_time
    )
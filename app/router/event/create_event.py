from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse


from schemas.event import EventCreateRequest, EventCreateResponse

router = APIRouter()

@router.post("/create", response_model=EventCreateResponse, status_code=status.HTTP_201_CREATED)
def create_event(request: Request, event_request: EventCreateRequest):
    response = EventCreateResponse(
        organizer_id=event_request.organizer_id,
        title=event_request.title,
        description=event_request.description, 
        start_time=event_request.start_time,
        end_time=event_request.end_time,
        venue_name=event_request.venue_name,
        venue_address=event_request.venue_address,
        total_tickets=event_request.total_tickets
    )
    return response
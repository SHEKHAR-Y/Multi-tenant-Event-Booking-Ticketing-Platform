# get all the events
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.event import EventService

router = APIRouter()

# get list of events
@router.get("/v1/event/get-all", status_code=status.HTTP_200_OK)
async def get_all_events(request: Request, db:AsyncSession =Depends(get_db)):
    eventservice = EventService(db=db)

    result = await eventservice.get_all_events()
    return result 


# get event with a particular id
@router.get("/v1/event/{event_id}", status_code=status.HTTP_200_OK)
async def get_event(request: Request, event_id: str, db: AsyncSession = Depends(get_db)):
    eventservice = EventService(db=db)

    result = await eventservice.get_event(event_id=event_id)
    return result 

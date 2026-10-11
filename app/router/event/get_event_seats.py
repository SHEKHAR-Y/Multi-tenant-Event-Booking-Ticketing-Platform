from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.event import EventService

router = APIRouter()


@router.get("/v1/event-seats/{event_id}", status_code=status.HTTP_200_OK)
async def get_event_seats(request: Request, event_id: str, db: AsyncSession = Depends(get_db)):
    eventservice = EventService(db=db)

    return await eventservice.get_all_event_seats(event_id=event_id)
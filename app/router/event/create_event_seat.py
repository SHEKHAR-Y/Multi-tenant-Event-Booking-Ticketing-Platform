from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.seat import BulkSeatCreationRequest
from app.services.event import EventService

router = APIRouter()


@router.post("/v1/event/create-seats", status_code=status.HTTP_201_CREATED)
async def create_bulk_seats_for_event(request: Request, seat: BulkSeatCreationRequest, current_user=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    eventservice = EventService(db=db)
    result = await eventservice.create_event_seats_in_bulk(seat_details=seat, current_user=current_user)
    if not result:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "event creation failed"}
        )

    return JSONResponse(
        content={"status": "success"}
    ) 

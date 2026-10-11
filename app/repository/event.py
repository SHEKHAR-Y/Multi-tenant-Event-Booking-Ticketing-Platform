from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.models.seat import Seat
from app.schemas.seat import SeatDetails


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(self, event: Event) -> Event:
        self.db.add(event)
        await self.db.flush()

        return event

    async def get_event_by_id(self, event_id: UUID) -> Event | None:
        statement = select(Event).where(Event.id == event_id)
        return await self.db.scalar(statement)
    
    async def get_all_events(self) -> list[Event] | None:
        statement = select(Event)

        results = await self.db.scalars(statement=statement)
        return results.all()

    async def get_event_with_id(self, id: UUID) -> Event | None:
        statement = select(Event).where(Event.id == id)

        return await self.db.scalar(statement=statement)

    async def create_seats_for_event(self, event_id: UUID, seat_list: list[SeatDetails]) -> bool:
        try : 
            seat_for_event = [
                {
                    "event_id": event_id,
                    "row":rows.row,
                    "seat_number":rows.seat_number,
                    "price":rows.price,
                }
                for rows in seat_list
            ]
            await self.db.execute(insert(Seat),seat_for_event)
            await self.db.flush()
            return True
        except :
            return False

    async def get_event_seats(self, event_id: UUID) -> list[Seat] | None:
        statement = select(Seat).where(Seat.event_id == event_id)

        results = await self.db.scalars(statement=statement)
        return results.all()
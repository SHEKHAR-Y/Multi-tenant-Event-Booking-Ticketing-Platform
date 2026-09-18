from sqlalchemy.orm import Session
from sqlalchemy import insert, select

from app.models.event import Event
from app.models.seat import Seat

from uuid import UUID

from app.schemas.seat import SeatDetails

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event: Event) -> Event:
        self.db.add(event)
        self.db.flush()

        return event

    def get_event_by_id(self, event_id: UUID) -> Event | None:
        statement = select(Event).where(Event.id == event_id)
        return self.db.scalar(statement)

    def creat_seats_for_event(self, event_id: UUID, seat_list: list[SeatDetails]) -> bool:
        seat_for_event = [
            {
                "event_id": event_id,
                "row":rows.row,
                "seat_number":rows.seat_number,
                "price":rows.price,
            }
            for rows in seat_list
        ]
        self.db.execute(insert(Seat),seat_for_event)
        self.db.flush()

        return True
from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.seat import Seat
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
    
    def get_all_events(self) -> list[Event] | None:
        statement = select(Event)

        return self.db.scalars(statement=statement).all()

    def creat_seats_for_event(self, event_id: UUID, seat_list: list[SeatDetails]) -> bool:
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
            self.db.execute(insert(Seat),seat_for_event)
            self.db.flush()
            return True
        except :
            return False

    def get_event_seats(self, event_id: UUID) -> list[Seat] | None:
        statement = select(Seat).where(Seat.event_id == event_id)

        result = self.db.scalars(statement=statement).all()
        return result
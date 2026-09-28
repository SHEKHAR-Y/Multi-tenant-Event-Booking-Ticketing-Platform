from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.seat import Booking, Seat, SeatStatus


class SeatRepository:
    def __init__(self, db: Session):
        self.db = db

    def check_seats_available(self, ids: list[UUID]) -> bool:
        number_of_seats = len(ids)
        statement = select(Seat).where(Seat.id.in_(ids)).with_for_update()
        seats = self.db.scalars(statement).all()

        if number_of_seats != len(seats):
            return False

        for i in ids:
            statement = select(Seat).where(Seat.id == i)

            seat = self.db.scalar(statement=statement)
            if seat.status != "available":
                return False

        return True

    def book_seats(self, ids: list[UUID], user_id: UUID, event_id: UUID):
        for i in ids:
            booking = Booking(
                seat_id = i, 
                event_id = event_id ,
                user_id = user_id
            )

            self.db.add(booking)
            # update the status of the seat to booked
            statement = select(Seat).where(Seat.id == i)
            currentseat = self.db.scalar(statement)

            currentseat.status = SeatStatus.BOOKED

        self.db.flush()
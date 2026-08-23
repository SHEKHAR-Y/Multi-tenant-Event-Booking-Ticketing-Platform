from sqlalchemy.orm import Session

from app.models.event import Event

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event: Event) -> Event:
        self.db.add(event)
        self.db.flush()

        return event
from pydantic import BaseModel, Field

from uuid import UUID

from decimal import Decimal

class SeatDetails(BaseModel):
    row: str = Field(min_length=1, max_length=4)
    seat_number: int = Field(gt=0)
    price: Decimal 

class BulkSeatCreationRequest(BaseModel):
    event_id: UUID
    seats: list[SeatDetails]

class SeatCreationResponse(BaseModel):
    id: UUID
    event_id: UUID
    row: str = Field(min_length=1, max_length=4)
    seat_number: int = Field(gt=0)
    price: Decimal 
    status: str
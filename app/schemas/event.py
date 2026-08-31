from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from uuid import UUID

class EventCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100, description="Title of the event")
    description: str = Field(min_length=10, max_length=1000, description="Description of the event")
    venue_name: str = Field(min_length=2, max_length=100, description="Name of the venue")
    venue_address: str = Field(min_length=5, max_length=200, description="Address of the venue")
    start_time: datetime = Field(description="Start time of the event in ISO 8601 format")
    end_time: datetime = Field(description="End time of the event in ISO 8601 format")

    @model_validator(mode="after")
    def check_end_after_start(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self
    
class EventCreateResponse(BaseModel):
    event_id: UUID = Field()
    organizer_id: UUID = Field(description="ID of the user creating the event")
    title: str = Field(min_length=3, max_length=100, description="Title of the event")
    description: str = Field(min_length=10, max_length=1000, description="Description of the event")
    venue_name: str = Field(min_length=2, max_length=100, description="Name of the venue")
    venue_address: str = Field(min_length=5, max_length=200, description="Address of the venue")
    start_time: datetime = Field(description="Start time of the event in ISO 8601 format")
    end_time: datetime = Field(description="End time of the event in ISO 8601 format")
    